import pygame
import kinect
import sys
from pykinect import nui
from pykinect.nui import JointId
import itertools

#Initialize sensors
#select data sources
#handle the data you read
LEFT_ARM = (JointId.ShoulderCenter, 
            JointId.ShoulderLeft, 
            JointId.ElbowLeft, 
            JointId.WristLeft, 
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter, 
             JointId.ShoulderRight, 
             JointId.ElbowRight, 
             JointId.WristRight, 
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter, 
            JointId.HipLeft, 
            JointId.KneeLeft, 
            JointId.AnkleLeft, 
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter, 
             JointId.HipRight, 
             JointId.KneeRight, 
             JointId.AnkleRight, 
             JointId.FootRight)
SPINE = (JointId.HipCenter, 
         JointId.Spine, 
         JointId.ShoulderCenter, 
         JointId.Head)



class GameRuntime(object):
    screen_lock = thread.allocate()
    def __init__(self):
        ##Game
        pygame.init()
        self.done = False
        
        ##Screen
        self.screenHeight = 960
        self.screenWidth = 540
        #actual screen has half height and width??
        self.screen = pygame.display.set_mode((self.screenHeight,self.screenWidth))
        #main surface from which to draw objects on screen
        self.frameSurface = pygame.Surface((self.kinect.color_frame_desc.Width,
                self.kinect.color_frame_desc.Height),0,32)
        
        ##Sensors, add more as we go
        self.kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FramSourceTypes_Color | \
        PyKinectV2.FrameSourceTypes_Body|PyKinectV2.FrameSourceTypes_Depth)
        
        # with nui.Runtime() as kinect:
        #     kinect.depth_frame_ready += depth_frame_ready   
        #     kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, 
        #         nui.ImageResolution.Resolution960x540, nui.ImageType.Depth)
        
        ##Skeleton
        self.bodies = None
        #hand heights
        self.curLHandX = self.curLHandY = self.curLHandZ = 0
        self.curRHandX = self.curRHandY = self.curRHandZ = 0
        self.curLElbX = self.curLElbY = self.curLElbZ = 0
        self.curRElbX = self.curRElbY = self.curRElbZ = 0
        
        #keep track of time to update screen
        self.clock = pygame.time.Clock()
    
    def depth_frame_ready(frame):
        with screen_lock:
            # Copy raw data in a temp surface
            frame.image.copy_bits(tmp_s._pixels_address)
            # Get actual depth data in mm
            #cut off first 3 insig bits, cut off most sig bit
            arr2d = (pygame.surfarray.pixels2d(tmp_s) >> 3) & 4095
    
    def checkGameDone(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
               
    def checkJointStatus(joints):
        #check if joints are correctly tracked before calculating
        if (joints[PyKinectV2.JointType_HandLeft].TrackingState == \
            PyKinectV2.TrackingState_NotTracked) or \
            (joints[PyKinectV2.JointType_HandRight].TrackingState == \
            PyKinectV2.TrackingState_NotTracked) or \
            (joints[PyKinectV2.JointType_ElbowLeft].TrackingState == \
            PyKinectV2.TrackingState_NotTracked) or \
            (joints[PyKinectV2.JointType_ElbowRight].TrackingState == \
            PyKinectV2.TrackingState_NotTracked):
                return False
        else: return True

    def recordHandPos(self,joints):
        leftHand = joints[PyKinectV2.JointType_HandLeft]
        rightHand = joints[PyKinectV2.JointType_HandRight]
        (self.curLHandX,self.curLHandY,self.curLHandZ) = (leftHand.Position.x, leftHand.Position.y,
                                    leftHand.Position.z)
        (self.curRHandX,self.curRHandY,self.curRHandZ) = (rightHand.Position.x, rightHand.Position.y,
                                    rightHand.Position.z)
        (self.curLElbX,self.curLElbY,self.curLElbZ) = (leftElbow.Position.x, leftElbow.Position.y,
                                    leftElbow.Position.z)
        (self.curRElbX,self.curRElbY,self.curRElbZ) = (rightElbow.Position.x,
                        rightElbow.Position.y,rightElbow.Position.z)

    def drawColorFrame(self, frame, targetSurface):
        #built-in function to display video with color
        targetSurface.lock()
        address = self.kinect.surface_as_array(targetSurface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        targetSurface.unlock()

    def stopGame(self):
        #observe player's hand motions to see if to quit game
        pass
        
    def depth_frame_ready(frame):
        frame.image.copy_bits(tmp_s._pixels_address)
    
        arr2d = (pygame.surfarray.pixels2d(tmp_s) >> 3) & 4095
        # arr2d[x,y] is the actual depth measured in mm at (x,y)
    
    def updateScreen(self):
        #built-in functino to update screen with colors
        h_to_w = float(self.frameSurface.get_height()) /
                                self._frame_surface.get_width()
        target_height = int(h_to_w * self._screen.get_width())
        surface_to_draw = pygame.transform.scale(self.frameSurface,
                        (self._screen.get_width(), target_height));   
        self.screen.blit(surface_to_draw, (0,0))
        surface_to_draw = None
        pygame.display.update()

    def run(self):
        while not self.done:
            checkGameDone()
            self.clock.tick(60)
            
            #if detect body
            if self.kinect.has_new_body_frame():
                self.bodies = self.kinect.get_last_body_frame()
                #double check that there is a body
                if self.bodies != None:
                    #only record one player
                    body = self.bodies.bodies[0]
                if body.is_tracked:
                    joints = body.joints
                    if checkJointStatus(joints):
                        recordHandPos(joints)
            if self.kinect.has_new_color_frame():
                frame = self.kinect.get_last_color_frame()
                self.draw_color_frame(frame, self.frame_surface)
                frame = None
            updateScreen()

            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            self._clock.tick(60)
        #once game done, stop kinect and quit game
        self.kinect.close()
        pygame.quit()
            
    
                
    
                
game = GamRuntime()
game.run()