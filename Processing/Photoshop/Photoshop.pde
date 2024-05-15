/**   DM Filter Project Starter Code
/*    v.20131126
/*    Bradley Beth
**/
boolean PicLoaded = false;
boolean Grayscale = false;
boolean Effect1 = false;
boolean Effect2 = false;
boolean Effect3 = false;
int picWidth = 0;
int picHeight = 0;
PImage img;
float r,g,b,a,c,d,x,y,z; 
/***********************************/
void setup() 
{
  size(800, 480);
  background(185);
  textAlign(LEFT);
  textSize(16); 
}
void draw()
{
  background(185);
  noStroke();
  int picStart = 0;
  int picEnd = 0;
  
  /* draw buttons */
  stroke(0);
  fill(0);
  textSize(16);
  text("File Operations",665,30);
  line(650,0,650,480);
  noStroke();
  
  fill(255);
  rect(660, 50, 130, 40, 10);
  fill(55);
  text("Load Picture", 675, 75);
  fill(255);
  rect(660, 100, 130, 40, 10);
  fill(55);
  text("Save Picture", 675, 125);
  stroke(0);
  line(650,150,800,150);
  noStroke();
  stroke(0);
  fill(0);
  textSize(16);
  text("Filter Effects",675,180);
  line(650,0,650,480);
  noStroke();
  if (Grayscale)
  {
    fill(#FFFF7D);    //Effect on means a yellow lighted button
  }
  else
  {
    fill(255);
    rect(660, 200, 130, 40, 10);
    fill(55);
    text("Grayscale", 680, 225);
  }
  
  if (Effect1)
  {
    fill(#FFFF7D);    //Effect on means a yellow lighted button 
  }  
  else
  {
    fill(255);
    rect(660, 250, 130, 40, 10);
    fill(55);
    text("Colorscale", 680, 275);
  }
  if (Effect2)
  {
    fill (#FFFF7D);      //Effect on means a yellow lighted button
  }
  else
  {
    fill(255); 
    rect(660, 300, 130, 40, 10);
    fill(55);
    text("Effect Two", 680, 325);
  }
  if (Effect3)
  {
    fill (#FFFF7D);    //Effect on means a yellow lighted button
  }
  else
  {
    fill(255);   
    rect(660, 350, 130, 40, 10);
    fill(55);
    text("Pixelate", 680, 375);
  }
  noStroke();
  textSize(16);
  //The following loads and displays an image file.
  //The image is resized to best fit in a 640x480 frame.
  if (PicLoaded)
  {     
    picWidth = img.width;
    picHeight = img.height;
    
    if (picWidth > 640)
    {
      picHeight = (int)(picHeight*(640.0/picWidth));
      picWidth = 640;
    }
    if (picHeight > 480)
    {
      picWidth = (int)(picWidth*(480.0/picHeight));
      picHeight = 480;
    }
    image(img, 0, 0, picWidth, picHeight);
    
    picStart = 0;
    picEnd = picStart+width*picHeight;
    
    /***** Effects Code *****/
    
    /* This sample grayscale code may serve as an example */
    if (Grayscale)
    {
      loadPixels();
      int i = picStart;
      while (i < picEnd) 
      {
        color c = pixels[i];
        float gray = (red(c)+green(c)+blue(c))/3.0;  //average the RGB colors
        pixels[i] = color(gray, gray, gray);
        i = i + 1;
        if (i % width >= picWidth)         // This will ignore anything on the line that 
          i = i + width - picWidth;        // after the image (such as buttons)
      }   
    }
    if (Effect1)
    {
      loadPixels();      
      int i = picStart;
      while (i < picEnd) 
       {
         // Get the R, G, B values from the image
         r = red  (pixels[i]);
         g = green(pixels[i]);
         b = blue (pixels[i]);
         r = r+a;
         g = g+c;
         b = b+d;
         color newColor = color(r,g,b);          //create a new color
         pixels[i] = newColor;            //store the new color  
         i = i + 1;                //next!
         if (i % width >= picWidth)         // This will ignore anything on the line that 
         {
           i = i + width - picWidth;        // after the image (such as buttons)
         }
       }
       updatePixels();                           //update the image
       if (keyPressed)
       {
         if (key == 'r')
         {
           a = a+1;
         }
         if (key == 'g')
         {
           c = c+1;
         }
         if (key == 'b')
         {
           d = d+1;
         }
         if (key == 'R')
         {
           a = a-1;
         }
         if (key == 'G')
         {
           c = c-1;
         }
         if (key == 'B')
         {
           d = d-1;
         }
         if (r < 0)
         {
           r = 0;
           x = 0;
         }
         if (b < 0)
         {
           b = 0;
           y = 0;
         }
         if (g < 0)
         {
           g = 0;
           z = 0;
         }
         if (r > 225)
         {
           r = 225;
           x = 225;
         }
         if (b > 225)
         {
           b = 225;
           y = 225;
         }
         if (g > 225)
         {
           g = 225;
           z = 225;
         }
       }      
    }
    println(r,g,b);
    updatePixels();                           
    if (Effect2)
    {
      loadPixels();      
      int i = picStart;
      while (i < picEnd) 
      {    
       r = red  (pixels[i]);
       g = green(pixels[i]);
       b = blue (pixels[i]);
       color newColor = color(r-20,g-20,b+40);          
       pixels[i] = newColor;              
       i = i + 1;    //next!
       if (i % width >= picWidth)
       {
          i = i + width - picWidth; 
       }
     }   
   }    
   if (Effect3)
   {
     loadPixels();      
     int i = picStart;
     while (i < picEnd) 
     {
       if (i % 20 == 0)
       {
         r = red  (pixels[i]);
         g = green(pixels[i]);
         b = blue (pixels[i]);
       }
       color newColor = color(r-0,g-0,b+0);          
       i = i + 1;    
       if (i % width >= picWidth) 
       {
         i = i + width - picWidth; 
       }   
     }
   }
   updatePixels(); 
   redraw();
   fill(255);
   noStroke();
   }
 }
void mouseClicked() 
{  
  redraw();
}
void mousePressed()
{
  
  
  if (mouseX>660 && mouseX<790 && mouseY>50 && mouseY<90)
  {
    selectInput("Select a file to process:", "infileSelected");
  }
  
  if (mouseX>660 && mouseX<790 && mouseY>100 && mouseY<140)
  {
    selectOutput("Select a file to write to:", "outfileSelected");
  }
  
  if (mouseX>660 && mouseX<790 && mouseY>200 && mouseY<240 && PicLoaded)
  {
    Grayscale = true;
    Effect1 = false;
    Effect2 = false;
    Effect3 = false;
  }   
  
  if (mouseX>660 && mouseX<790 && mouseY>250 && mouseY<290 && PicLoaded)
  {
    Effect1 = true;
    Grayscale = false;
    Effect2 = false;
    Effect3 = false;
  } 
  if (mouseX>660 && mouseX<790 && mouseY>300 && mouseY<340 && PicLoaded)
  {
    Effect2 = true;
    Grayscale = false;
    Effect1 = false;
    Effect3 = false;
  }  
  if (mouseX>660 && mouseX<790 && mouseY>350 && mouseY<390 && PicLoaded)
  {
    Effect3 = true;
    Grayscale = false;
    Effect1 = false;
    Effect2 = false;
    
  } 
  redraw();
}
void infileSelected(File selection) 
{
  if (selection == null) 
  {
    println("IMAGE NOT LOADED: Window was closed or the user hit cancel.");
  } 
  else 
  {
    println("IMAGE LOADED: User selected " + selection.getAbsolutePath());
    img = loadImage(selection.getAbsolutePath());
    PicLoaded = true;
    Grayscale = false;
    Effect1 = false;
    Effect2 = false;
    Effect3 = false;
    redraw();
  }
}
void outfileSelected(File selection) 
{
  if (selection == null) 
  {
    println("IMAGE NOT SAVED: Window was closed or the user hit cancel.");
  } 
  else 
  {
    println("IMAGE SAVED: User selected " + selection.getAbsolutePath());
    updatePixels();
    redraw();
    save(selection.getAbsolutePath());
    redraw();
  }
}