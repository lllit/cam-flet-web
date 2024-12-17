#from flet import *
import cv2
import time
import os
import base64


cam_running = True


from flet import *


def main(page: Page):
    page.scroll = ScrollMode.ADAPTIVE
    page.appbar = AppBar(title=Text("PermissionHandler Tests"))
    ph = PermissionHandler()
    page.overlay.append(ph)

    def check_permission(e):
        o = ph.check_permission(e.control.data)
        page.add(Text(f"Checked {e.control.data.name}: {o}"))

    def request_permission(e):
        o = ph.request_permission(e.control.data)
        page.add(Text(f"Requested {e.control.data.name}: {o}"))

    def open_app_settings(e):
        o = ph.open_app_settings()
        page.add(Text(f"App Settings: {o}"))


    image_default_path = base64.b64encode(open("./assets/camara.png", 'rb').read()).decode("utf-8")


    myimage = Image(
        expand=True,
        src_base64=image_default_path,
        src=False,
        fit=ImageFit.COVER
    )

    def stop_camera(e):
        global cam_running
        cam_running = False
        # if myimage and image_default_path:
        #     myimage.src_base64 = image_default_path
        #     print("Camara stop")
        myimage.src_base64 = image_default_path  
        page.update()
    def remove_all_pic():
        folder_path = "fotos/"
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print("Archivo eliminado con exito")
        page.update()


    # Tomar foto
    def take_pic(e):
        remove_all_pic()
        global cam_running
    
        cap = cv2.VideoCapture(0)
    
        timeStamp = str(int(time.time()))
        myfileface = str(f"myCumFace_{timeStamp}.jpg")
        try:
            while cam_running:
                ret, frame = cap.read()
                if ret:
                    _, buffer = cv2.imencode('.png', frame)
                    frame_base64 = base64.b64encode(buffer).decode('utf-8')
                    myimage.src_base64 = frame_base64
                    page.update()


                key = cv2.waitKey(1)
                if key == ord("q"):
                    break
                elif key == ord("s"):
                    cv2.imwrite(f"fotos/{myfileface}", frame)
                
                    folder_path = "fotos/"
                    myimage.src_base64 = f"{folder_path}{myfileface}"
                    page.update()
                    break
        
            page.update()
        except Exception as e:
            print(f"Error: {e}")

    # Abrir la camara
    def scann_qr(e):
        image_default_path = base64.b64encode(open("./assets/camara.png", 'rb').read()).decode("utf-8")

        
    cam_view = Column(
        controls=[
            Text("Webcam", size=30, weight=FontWeight.BOLD),
            ElevatedButton("Tomar foto", bgcolor=Colors.BLUE_400, color=Colors.WHITE, on_click=take_pic),
            # ElevatedButton("Escann", bgcolor=Colors.BLUE_500, color=Colors.WHITE, on_click=scann_qr),
            ElevatedButton("Cerrar Camara", bgcolor=Colors.BLUE_900, color=Colors.WHITE, on_click=stop_camera),
            myimage
        ]
    )

    page.add(

        cam_view,
        OutlinedButton(
            "Check Cam Permission",
            data=PermissionType.CAMERA,
            on_click=check_permission,
        ),
        OutlinedButton(
            "Request Camara Permission",
            data=PermissionType.CAMERA,
            on_click=request_permission,
        ),
        OutlinedButton(
            "Open App Settings",
            on_click=open_app_settings,
        ),
    )


app(target=main, assets_dir="assets", view=WEB_BROWSER)
