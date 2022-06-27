let width;
let height;

function preload(){
  img = loadImage("pic/sky.jpg");
  airplane = loadImage("pic/plane.png")
}


function setup() {
  createCanvas(window.innerWidth, window.innerHeight)
  // let Canvas = createCanvas(window.innerWidth, window.innerHeight);
  // Canvas.parent('canvas-container');
  width = window.innerWidth
  height = window.innerHeight
  noCursor();
}

function draw() {
  background(255, 246, 212);
  drawsky()
  image(airplane, mouseX, mouseY, 80, 80);
}

function drawsky(){
  noStroke();
      image(img, 0, 0, width, height) ;
  
}