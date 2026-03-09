#include "HID-Project.h"
#include <hidboot.h>
#include <usbhub.h>

USB Usb;
USBHub Hub(&Usb);
HIDBoot < USB_HID_PROTOCOL_KEYBOARD | USB_HID_PROTOCOL_MOUSE > HidComposite(&Usb);
HIDBoot<USB_HID_PROTOCOL_MOUSE> HidMouse(&Usb);

class MouseRptParser : public MouseReportParser {
  protected:
    void OnMouseMove(MOUSEINFO *mi) { Mouse.move(mi->dX, mi->dY); };
    void OnLeftButtonUp(MOUSEINFO *mi)    { Mouse.release(MOUSE_LEFT); }
    void OnLeftButtonDown(MOUSEINFO *mi)  { Mouse.press(MOUSE_LEFT); }
    void OnRightButtonUp(MOUSEINFO *mi)   { Mouse.release(MOUSE_RIGHT); }
    void OnRightButtonDown(MOUSEINFO *mi) { Mouse.press(MOUSE_RIGHT); }
    void OnMiddleButtonUp(MOUSEINFO *mi)  { Mouse.release(MOUSE_MIDDLE); }
    void OnMiddleButtonDown(MOUSEINFO *mi) { Mouse.press(MOUSE_MIDDLE); }
    virtual void Parse(USBHID *hid, bool is_rpt_id, uint8_t len, uint8_t *buf) {
      MouseReportParser::Parse(hid, is_rpt_id, len, buf);
      if (len > 3) {
        int8_t wheelMovement = (int8_t)buf[3];
        if (wheelMovement != 0) {
          Mouse.move(0, 0, wheelMovement);
        }
      }
    };
};
MouseRptParser MousePrs;

void setup() {
  Mouse.begin();
  Serial.begin(115200);
  Usb.Init();
  HidComposite.SetReportParser(1, &MousePrs);
  HidMouse.SetReportParser(0, &MousePrs);
}


void moverEnBatches(int xTotal, int yTotal) {
  int pasoMaximo = 8;
  while (xTotal != 0 || yTotal != 0) {
    int dx = 0;
    int dy = 0;

    if (xTotal > 0) {
      dx = (xTotal >= pasoMaximo) ? pasoMaximo : xTotal;
    } else if (xTotal < 0) {
      dx = (xTotal <= -pasoMaximo) ? -pasoMaximo : xTotal;
    }


    if (yTotal > 0) {
      dy = (yTotal >= pasoMaximo) ? pasoMaximo : yTotal;
    } else if (yTotal < 0) {
      dy = (yTotal <= -pasoMaximo) ? -pasoMaximo : yTotal;
    }

    Mouse.move(dx, dy);

    xTotal -= dx;
    yTotal -= dy;

    delayMicroseconds(200); 
  }
}

void loop() {
  Usb.Task();

  if (Serial.available() > 0) {
    int xTarget = Serial.parseInt();
    int yTarget = Serial.parseInt();

    if (xTarget != 0 || yTarget != 0) {
      moverEnBatches(xTarget, yTarget);
      
      Keyboard.press('a'); 
      Mouse.press(MOUSE_LEFT);
      Mouse.release(MOUSE_LEFT); 
      Keyboard.release('a');
    }
    
    // Limpiamos el buffer serial para evitar lecturas fantasmas
    while(Serial.available() > 0) Serial.read();
  }
}
