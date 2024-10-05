import json
import os
import cv2
from random import randrange

COLORS_10 =[(144,238,144),(178, 34, 34),(221,160,221),(  0,255,  0),(  0,128,  0),(210,105, 30),(220, 20, 60),
            (192,192,192),(255,228,196),( 50,205, 50),(139,  0,139),(100,149,237),(138, 43,226),(238,130,238),
            (255,  0,255),(  0,100,  0),(127,255,  0),(255,  0,255),(  0,  0,205),(255,140,  0),(255,239,213),
            (199, 21,133),(124,252,  0),(147,112,219),(106, 90,205),(176,196,222),( 65,105,225),(173,255, 47),
            (255, 20,147),(219,112,147),(186, 85,211),(199, 21,133),(148,  0,211),(255, 99, 71),(144,238,144),
            (255,255,  0),(230,230,250),(  0,  0,255),(128,128,  0),(189,183,107),(255,255,224),(128,128,128),
            (105,105,105),( 64,224,208),(205,133, 63),(  0,128,128),( 72,209,204),(139, 69, 19),(255,245,238),
            (250,240,230),(152,251,152),(  0,255,255),(135,206,235),(  0,191,255),(176,224,230),(  0,250,154),
            (245,255,250),(240,230,140),(245,222,179),(  0,139,139),(143,188,143),(255,  0,  0),(240,128,128),
            (102,205,170),( 60,179,113),( 46,139, 87),(165, 42, 42),(178, 34, 34),(175,238,238),(255,248,220),
            (218,165, 32),(255,250,240),(253,245,230),(244,164, 96),(210,105, 30)]
videoInfo = {"cam_1": {"frame_num": 3000, "movement_num": 4},
             "cam_1_dawn": {"frame_num": 3000, "movement_num": 4},
             "cam_1_rain": {"frame_num": 2961, "movement_num": 4},
             "cam_2": {"frame_num": 18000, "movement_num": 4},
             "cam_2_rain": {"frame_num": 3000, "movement_num": 4},
             "cam_3": {"frame_num": 18000, "movement_num": 4},
             "cam_3_rain": {"frame_num": 3000, "movement_num": 4},
             "cam_4": {"frame_num": 27000, "movement_num": 12},
             "cam_4_dawn": {"frame_num": 4500, "movement_num": 12},
             "cam_4_rain": {"frame_num": 3000, "movement_num": 12},
             "cam_5": {"frame_num": 18000, "movement_num": 12},
             "cam_5_dawn": {"frame_num": 3000, "movement_num": 12},
             "cam_5_rain": {"frame_num": 3000, "movement_num": 12},
             "cam_6": {"frame_num": 18000, "movement_num": 12},
             "cam_6_snow": {"frame_num": 3000, "movement_num": 12},
             "cam_7": {"frame_num": 14400, "movement_num": 12},
             "cam_7_dawn": {"frame_num": 2400, "movement_num": 12},
             "cam_7_rain": {"frame_num": 3000, "movement_num": 12},
             "cam_8": {"frame_num": 3000, "movement_num": 6},
             "cam_9": {"frame_num": 3000, "movement_num": 12},
             "cam_10": {"frame_num": 2111, "movement_num": 3},
             "cam_11": {"frame_num": 2111, "movement_num": 3},
             "cam_12": {"frame_num": 1997, "movement_num": 3},
             "cam_13": {"frame_num": 1966, "movement_num": 3},
             "cam_14": {"frame_num": 3000, "movement_num": 2},
             "cam_15": {"frame_num": 3000, "movement_num": 2},
             "cam_16": {"frame_num": 3000, "movement_num": 2},
             "cam_17": {"frame_num": 3000, "movement_num": 2},
             "cam_18": {"frame_num": 3000, "movement_num": 2},
             "cam_19": {"frame_num": 3000, "movement_num": 2},
             "cam_20": {"frame_num": 3000, "movement_num": 2}}

if __name__ == "__main__":
    # segment number
    n = 10 

    #jsonRoot = "C:/Users/Allen/Desktop/tracking/StrongSORT-YOLO/VehicleCounting/cam-configs"
    #imgRoot = "../screen_shot_with_roi_and_movement_tucson/"
    #visRoot = "../vis_tucson/"
    # for vId, vName in enumerate(videoInfo.keys()):

    camName = "frame0" #"cam_" + vName.split("_")[1]
    img = cv2.imread("frame0.jpg")
    #with open("C:/Users/Allen/Desktop/tracking/StrongSORT-YOLO/VehicleCounting/cam-configs/cam.json") as fp:
    #    camJson = json.load(fp)
    #load tracks
    tracks = {}
    track_file = "Tucson.txt"
    #data_root = "C:/Users/Allen/Desktop/tracking/StrongSORT-YOLO"
    #path to track results path
    #track_file = os.path.join(data_root, "Tucson.txt")
    with open(track_file, 'r') as ft:
        lines = [line.strip('\n').split(' ') for line in ft]
        for line in lines:
            frameid = int(line[0])
            trackid = int(line[2])
            x1 = int(float(line[3]))
            y1 = int(float(line[4]))
            x2 = int(float(line[5]))+x1
            y2 = int(float(line[6]))+y1
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            obj_cls = line[1]
            if trackid in tracks: #update
                tracks[trackid]['endframe'] = frameid
                tracks[trackid]['bbox'].append([frameid, x1, y1, x2, y2, obj_cls])
                tracks[trackid]['tracklet'].append([cx, cy])
            else:
                tracks[trackid] = {'startframe' : frameid,
                                   'endframe' : frameid,
                                   'bbox' : [[frameid, x1, y1, x2, y2, obj_cls]],
                                   'tracklet' : [[cx, cy]]}

    moi = {} 
    moi["movement_1"] = {} #v
    moi["movement_1"]["tracklets"] = [tracks[314]['tracklet']] 
    moi["movement_1"]["src"] = {}
    moi["movement_1"]["dst"] = {}
    moi["movement_1"]["src"]["point_1"] = [10,197]
    moi["movement_1"]["src"]["point_2"] = [57,179]
    moi["movement_1"]["src"]["exclusive_relationship"] = "1_s"
    moi["movement_1"]["dst"]["point_1"] = [327,699]
    moi["movement_1"]["dst"]["point_2"] = [495,566]
    moi["movement_1"]["dst"]["exclusive_relationship"] = "1_e"


    moi["movement_2"] = {} #v
    moi["movement_2"]["tracklets"] = [tracks[138]['tracklet'][200:]]
    moi["movement_2"]["src"] = {}
    moi["movement_2"]["dst"] = {}
    moi["movement_2"]["src"]["point_1"] = [62,178]
    moi["movement_2"]["src"]["point_2"] = [114,160]
    moi["movement_2"]["src"]["exclusive_relationship"] = "2_s"
    moi["movement_2"]["dst"]["point_1"] = [500,562]
    moi["movement_2"]["dst"]["point_2"] = [628,463]
    moi["movement_2"]["dst"]["exclusive_relationship"] = "2_e"


    moi["movement_3"] = {} #v
    moi["movement_3"]["tracklets"] = [tracks[6]['tracklet']]
    moi["movement_3"]["src"] = {}
    moi["movement_3"]["dst"] = {}
    moi["movement_3"]["src"]["point_1"] = [118,159]
    moi["movement_3"]["src"]["point_2"] = [172,142]
    moi["movement_3"]["src"]["exclusive_relationship"] = "3_s"
    moi["movement_3"]["dst"]["point_1"] = [637,457]
    moi["movement_3"]["dst"]["point_2"] = [762,361]
    moi["movement_3"]["dst"]["exclusive_relationship"] = "3_e"


    moi["movement_4"] = {} #v
    moi["movement_4"]["tracklets"] = [tracks[116]['tracklet']]
    moi["movement_4"]["src"] = {}
    moi["movement_4"]["dst"] = {}
    moi["movement_4"]["src"]["point_1"] = [179,140]
    moi["movement_4"]["src"]["point_2"] = [221,126]
    moi["movement_4"]["src"]["exclusive_relationship"] = "4_s"
    moi["movement_4"]["dst"]["point_1"] = [1004,134]
    moi["movement_4"]["dst"]["point_2"] = [1062,155]
    moi["movement_4"]["dst"]["exclusive_relationship"] = "4_e"


    moi["movement_5"] = {} #v
    moi["movement_5"]["tracklets"] = [tracks[544]['tracklet']]
    moi["movement_5"]["src"] = {}
    moi["movement_5"]["dst"] = {}
    moi["movement_5"]["src"]["point_1"] = [227,125]
    moi["movement_5"]["src"]["point_2"] = [265,111]
    moi["movement_5"]["src"]["exclusive_relationship"] = "5_s"
    moi["movement_5"]["dst"]["point_1"] = [956,120]
    moi["movement_5"]["dst"]["point_2"] = [1004,135]
    moi["movement_5"]["dst"]["exclusive_relationship"] = "5_e"


    moi["movement_6"] = {} #v
    moi["movement_6"]["tracklets"] = [tracks[109]['tracklet'][:-20]]
    moi["movement_6"]["src"] = {}
    moi["movement_6"]["dst"] = {}
    moi["movement_6"]["src"]["point_1"] = [682,45]
    moi["movement_6"]["src"]["point_2"] = [684,59]
    moi["movement_6"]["src"]["exclusive_relationship"] = "6_s"
    moi["movement_6"]["dst"]["point_1"] = [485,49]
    moi["movement_6"]["dst"]["point_2"] = [484,73]
    moi["movement_6"]["dst"]["exclusive_relationship"] = "6_e"


    moi["movement_7"] = {} #v
    moi["movement_7"]["tracklets"] = [tracks[8]['tracklet']]
    moi["movement_7"]["src"] = {}
    moi["movement_7"]["dst"] = {}
    moi["movement_7"]["src"]["point_1"] = [720,58]
    moi["movement_7"]["src"]["point_2"] = [745,70]
    moi["movement_7"]["src"]["exclusive_relationship"] = "7_s"
    moi["movement_7"]["dst"]["point_1"] = [55,201]
    moi["movement_7"]["dst"]["point_2"] = [82,238]
    moi["movement_7"]["dst"]["exclusive_relationship"] = "7_e"


    moi["movement_8"] = {} #v
    moi["movement_8"]["tracklets"] = [tracks[1]['tracklet']]
    moi["movement_8"]["src"] = {}
    moi["movement_8"]["dst"] = {}
    moi["movement_8"]["src"]["point_1"] = [709,76]
    moi["movement_8"]["src"]["point_2"] = [745,95]
    moi["movement_8"]["src"]["exclusive_relationship"] = "8_s"
    moi["movement_8"]["dst"]["point_1"] = [87,234]
    moi["movement_8"]["dst"]["point_2"] = [129,289]
    moi["movement_8"]["dst"]["exclusive_relationship"] = "8_e"

    moi["movement_9"] = {} #v
    moi["movement_9"]["tracklets"] = [tracks[350]['tracklet']]
    moi["movement_9"]["src"] = {}
    moi["movement_9"]["dst"] = {}
    moi["movement_9"]["src"]["point_1"] = [766,92]
    moi["movement_9"]["src"]["point_2"] = [810,108]
    moi["movement_9"]["src"]["exclusive_relationship"] = "9_s"
    moi["movement_9"]["dst"]["point_1"] = [645,350]
    moi["movement_9"]["dst"]["point_2"] = [744,311]
    moi["movement_9"]["dst"]["exclusive_relationship"] = "9_e"

    moi["movement_10"] = {} #v
    moi["movement_10"]["tracklets"] = [tracks[7]['tracklet']]
    moi["movement_10"]["src"] = {}
    moi["movement_10"]["dst"] = {}
    moi["movement_10"]["src"]["point_1"] = [826,103]
    moi["movement_10"]["src"]["point_2"] = [882,125]
    moi["movement_10"]["src"]["exclusive_relationship"] = "10_s"
    moi["movement_10"]["dst"]["point_1"] = [745,305]
    moi["movement_10"]["dst"]["point_2"] = [851,266]
    moi["movement_10"]["dst"]["exclusive_relationship"] = "10_e"

    moi["movement_11"] = {} #v
    moi["movement_11"]["tracklets"] = [tracks[250]['tracklet']]
    moi["movement_11"]["src"] = {}
    moi["movement_11"]["dst"] = {}
    moi["movement_11"]["src"]["point_1"] = [1198,237]
    moi["movement_11"]["src"]["point_2"] = [1184,282]
    moi["movement_11"]["src"]["exclusive_relationship"] = "11_s"
    moi["movement_11"]["dst"]["point_1"] = [512,74]
    moi["movement_11"]["dst"]["point_2"] = [464,88]
    moi["movement_11"]["dst"]["exclusive_relationship"] = "11_e"

    moi["movement_12"] = {} #v 
    moi["movement_12"]["tracklets"] = [tracks[248]['tracklet']]
    moi["movement_12"]["src"] = {}
    moi["movement_12"]["dst"] = {}
    moi["movement_12"]["src"]["point_1"] = [1183,289]
    moi["movement_12"]["src"]["point_2"] = [1170,336]
    moi["movement_12"]["src"]["exclusive_relationship"] = "12_s"
    moi["movement_12"]["dst"]["point_1"] = [460,89]
    moi["movement_12"]["dst"]["point_2"] = [403,105]
    moi["movement_12"]["dst"]["exclusive_relationship"] = "12_e"

    moi["movement_13"] = {} #v
    moi["movement_13"]["tracklets"] = [tracks[240]['tracklet']]
    moi["movement_13"]["src"] = {}
    moi["movement_13"]["dst"] = {}
    moi["movement_13"]["src"]["point_1"] = [1170,340]
    moi["movement_13"]["src"]["point_2"] = [1156,384]
    moi["movement_13"]["src"]["exclusive_relationship"] = "13_s"
    moi["movement_13"]["dst"]["point_1"] = [399,106]
    moi["movement_13"]["dst"]["point_2"] = [340,126]
    moi["movement_13"]["dst"]["exclusive_relationship"] = "13_e"

    moi["movement_14"] = {} #v
    moi["movement_14"]["tracklets"] = [tracks[423]['tracklet']]
    moi["movement_14"]["src"] = {}
    moi["movement_14"]["dst"] = {}
    moi["movement_14"]["src"]["point_1"] = [1155,397]
    moi["movement_14"]["src"]["point_2"] = [1139,462]
    moi["movement_14"]["src"]["exclusive_relationship"] = "14_s"
    moi["movement_14"]["dst"]["point_1"] = [477,220]
    moi["movement_14"]["dst"]["point_2"] = [442,318]
    moi["movement_14"]["dst"]["exclusive_relationship"] = "14_e"

    moi["movement_15"] = {} #v
    moi["movement_15"]["tracklets"] = [tracks[2]['tracklet']]
    moi["movement_15"]["src"] = {}
    moi["movement_15"]["dst"] = {}
    moi["movement_15"]["src"]["point_1"] = [123,392]
    moi["movement_15"]["src"]["point_2"] = [159,451]
    moi["movement_15"]["src"]["exclusive_relationship"] = "15_s"
    moi["movement_15"]["dst"]["point_1"] = [952,122]
    moi["movement_15"]["dst"]["point_2"] = [1001,140]
    moi["movement_15"]["dst"]["exclusive_relationship"] = "15_e"

    moi["movement_16"] = {} #v
    moi["movement_16"]["tracklets"] = [tracks[4]['tracklet']]
    moi["movement_16"]["src"] = {}
    moi["movement_16"]["dst"] = {}
    moi["movement_16"]["src"]["point_1"] = [167,464]
    moi["movement_16"]["src"]["point_2"] = [207,527]
    moi["movement_16"]["src"]["exclusive_relationship"] = "16_s"
    moi["movement_16"]["dst"]["point_1"] = [1003,137]
    moi["movement_16"]["dst"]["point_2"] = [1060,160]
    moi["movement_16"]["dst"]["exclusive_relationship"] = "16_e"

    moi["movement_17"] = {} #v
    moi["movement_17"]["tracklets"] = [tracks[9]['tracklet']]
    moi["movement_17"]["src"] = {}
    moi["movement_17"]["dst"] = {}
    moi["movement_17"]["src"]["point_1"] = [212,534]
    moi["movement_17"]["src"]["point_2"] = [274,621]
    moi["movement_17"]["src"]["exclusive_relationship"] = "17_s"
    moi["movement_17"]["dst"]["point_1"] = [1068,155]
    moi["movement_17"]["dst"]["point_2"] = [1135,181]
    moi["movement_17"]["dst"]["exclusive_relationship"] = "17_e"

    moi["movement_18"] = {} #v
    moi["movement_18"]["tracklets"] = [tracks[62]['tracklet']]
    moi["movement_18"]["src"] = {}
    moi["movement_18"]["dst"] = {}
    moi["movement_18"]["src"]["point_1"] = [78,321]
    moi["movement_18"]["src"]["point_2"] = [118,383]
    moi["movement_18"]["src"]["exclusive_relationship"] = "18_s"
    moi["movement_18"]["dst"]["point_1"] = [354,170]
    moi["movement_18"]["dst"]["point_2"] = [461,203]
    moi["movement_18"]["dst"]["exclusive_relationship"] = "18_e"

    moi["movement_19"] = {} #v
    moi["movement_19"]["tracklets"] = [tracks[586]['tracklet']]
    moi["movement_19"]["src"] = {}
    moi["movement_19"]["dst"] = {}
    moi["movement_19"]["src"]["point_1"] = [834,101]
    moi["movement_19"]["src"]["point_2"] = [886,124]
    moi["movement_19"]["src"]["exclusive_relationship"] = "19_s"
    moi["movement_19"]["dst"]["point_1"] = [1083,111]
    moi["movement_19"]["dst"]["point_2"] = [1159,157]
    moi["movement_19"]["dst"]["exclusive_relationship"] = "19_e"

    moi["movement_20"] = {} #v
    moi["movement_20"]["tracklets"] = [tracks[586]['tracklet']]
    moi["movement_20"]["src"] = {}
    moi["movement_20"]["dst"] = {}
    moi["movement_20"]["src"]["point_1"] = [1271,261]
    moi["movement_20"]["src"]["point_2"] = [1251,293]
    moi["movement_20"]["src"]["exclusive_relationship"] = "20_s"
    moi["movement_20"]["dst"]["point_1"] = [1095,176]
    moi["movement_20"]["dst"]["point_2"] = [1140,177]
    moi["movement_20"]["dst"]["exclusive_relationship"] = "20_e"


    camJson = moi
    for mName, moveInfo in camJson.items():
        colVal = tuple((randrange(255), randrange(255), randrange(255), 0.3))
        mId = int(mName.split("_")[-1])
        x1, y1 = moveInfo["src"]["point_1"]
        x2, y2 = moveInfo["src"]["point_2"]
        #import pdb;pdb.set_trace()
        cv2.line(img, (x1,y1), (x2,y2), colVal, 5) # draw start line
        cv2.putText(img, '%ds'%(mId), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1.2, colVal, 2)

        x3, y3 = moveInfo["dst"]["point_1"]
        x4, y4 = moveInfo["dst"]["point_2"]
        cv2.line(img, (x3,y3), (x4,y4), colVal, 5) # draw end line
        cv2.putText(img, '%de'%(mId), (x3, y3), cv2.FONT_HERSHEY_SIMPLEX, 1.2, colVal, 2)

        # draw tracklets
        tracklet_key = "tracklets"
        if tracklet_key in moveInfo.keys():
            for m_tracklet in moveInfo["tracklets"]:
                print(mId)
                #import pdb;pdb.set_trace()
                p0 = tuple(m_tracklet[0])
                cv2.putText(img, '%ds'%(mId), (int(p0[0]), int(p0[1])), cv2.FONT_HERSHEY_SIMPLEX, 1.2, colVal, 2)
                for i in range(1, len(m_tracklet)):
                    p1 = tuple(m_tracklet[i])
                    # cv2.line(img, p0, p1, colVal, 5)
                    cv2.arrowedLine(img, (int(p0[0]), int(p0[1])), (int(p1[0]), int(p1[1])), colVal, 2)
                    p0 = p1

    cv2.imwrite("res2.jpg", img)
    print("res2.jpg")
