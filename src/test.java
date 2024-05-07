
import java.util.ArrayList;

/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */

/**
 *
 * @author User
 */
public class test {
     public static void main(String args[]) 
     {
        ArrayList<user> users = new ArrayList<user>();
        user admin = new user();
        admin.setTendangnhap("cr7");
        admin.setMatkhau("cr7");
        users.add(admin);
        
        java.awt.EventQueue.invokeLater(new Runnable() {
            public void run() 
            {
                new Interface(users).setVisible(true);
            }
        });
        
     
     }
}
        
