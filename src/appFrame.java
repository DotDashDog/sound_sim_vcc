
import javax.swing.*;
import java.awt.*;

import static java.awt.Color.*;

public class appFrame extends JFrame {
    int windowSideLength = 1000;
    int x;
    int y;
    public appFrame() {
        init();
    }
    public void init() {
        Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
        int height = 10;
        int width = 10;
        setSize(height,width);
        repaint();
    }
    public void paint(Graphics g){
        int playerSize = 50;
        g.setColor(WHITE);
        g.fillRect(-1,-1,50000,50000);
        //drawMap(Graphics g);
        //drawMap doesn't work rn so cpy paste
        x = MouseInfo.getPointerInfo().getLocation().x;
        y = MouseInfo.getPointerInfo().getLocation().y;
        int mapH = 500;
        int mapW = 500;
        //this is the map part
        //where we draw the map tediously
        g.setColor(RED);
        g.drawRect(x-(mapW/2),y-(mapH/2),mapW,mapH);
        g.setColor(black);
        g.fillOval(500,500,playerSize,playerSize);
    }
    public void drawMap(Graphics g){
        x = MouseInfo.getPointerInfo().getLocation().x;
        y = MouseInfo.getPointerInfo().getLocation().y;
        int mapH = 500;
        int mapW = 500;
        //this is the map part
        //where we draw the map tediously
        g.setColor(RED);
        g.drawRect(x+(mapW/2),y+(mapH/2),mapW,mapH);
    }


}
