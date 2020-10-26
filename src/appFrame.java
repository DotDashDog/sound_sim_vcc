
import javax.swing.*;
import java.awt.*;

import static java.awt.Color.*;

public class appFrame extends JFrame {
    int windowSideLength = 1000;
    public appFrame() {
        init();
    }
    public void init() {
        setSize(10,10);
        repaint();
    }
    public void paint(Graphics g){
        int x = MouseInfo.getPointerInfo().getLocation().x;
        int y = MouseInfo.getPointerInfo().getLocation().y;
        g.setColor(white);
        g.fillRect(0,0,2000,1200);
        g.setColor(black);
        g.fillOval(x,y,50,50);
    }

}
