int filament=0;
int cost=0;
int density=0;
int diameter=0;
int filamentused=0;
int infil=0;
int filamentlength=0;
int price=0;
int printvolume=0;
int printweight=0;

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
  
  fill(255);
  rect(15, 10, 80, 40, 10);
  fill(0);
  textSize(16);
  text("Input",30,35);
  noStroke();
  
  stroke(0);
  line(400,0,400,480);
  noStroke();
  
  fill(255);
  rect(415, 10, 80, 40, 10);
  fill(0);
  textSize(16);
  text("Output",430,35);
  noStroke();
}