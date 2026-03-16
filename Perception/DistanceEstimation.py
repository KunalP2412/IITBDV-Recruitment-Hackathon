from ultralytics import YOLO
import cv2
model = YOLO('YOLOv11s-Carmaker.pt')
img=cv2.imread('cones.png')
results = model(img)
for result in results:
    boxes = result.boxes 
    for box in boxes:
        coords = box.xyxy[0].tolist() 
        x1,y1,x2,y2=coords
        id = box.cls[0].item()
        p_dist = (y2-y1)
        if(p_dist >0):
            distance = (30)*(1000)/p_dist

        x1,y1,x2,y2=int(x1),int(y1),int(x2),int(y2)
   
        class_id = int(box.cls[0].item())
        class_name = model.names[class_id]
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        dlabel = f"{distance:.2f}cm"
        cv2.putText(img, dlabel, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 255),1)
        cv2.putText(img, class_name, (x1, y1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 255, 255),1)
        cv2.imwrite('results.png', img)




