Population test;
PVector goal = new PVector(400,10);

void setup(){
  size(800,800);
  test = new Population(1000);
}

void draw(){
  background(255);
  fill(255,0,0);
  ellipse(goal.x,goal.y,10,10);
  
  //wall
  fill(0,0,225);
  rect(0,300,395,10);
  rect(405,300,395,10);
  rect(0,500,395,10);
  rect(405,500,395,10);
  rect(0,100,395,10);
  rect(405,100,395,10);
  rect(0,700,395,10);
  rect(405,700,395,10);
  
  if(test.allDotsDead()){
    //genetic algorithm
    test.calculateFitness();
    test.naturalSelection();
    test.mutateDemBabies();
  }else{
    test.update();
    test.show();
  }
}
