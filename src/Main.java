import java.awt.*;
import java.awt.event.WindowEvent;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

public class Main {
    public static void main(String[] args) throws InterruptedException {
        GraphicsDevice device = GraphicsEnvironment.getLocalGraphicsEnvironment().getScreenDevices()[0];

        appFrame a = new appFrame();
        a.setDefaultCloseOperation(appFrame.EXIT_ON_CLOSE);
        a.setVisible(true);
        device.setFullScreenWindow(a);
        while (true) {
            a.repaint();
            Thread.sleep(5);
        }

    }
}
