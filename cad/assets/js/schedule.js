var coefWidth = 0.575;
var windowSize = new vector2D();
var colWidth;
var nbCols = 8;
var scheds = [];
var users  = [];
var canvas;
var isPressed = false;
var lastMousePos = new vector2D();

function mobileAndTabletcheck() {
  var check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino|android|ipad|playbook|silk/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};

function vector2D(base_x=0, base_y=0){
  this.x = base_x;
  this.y = base_y;

  this.move_int = function(delta_x, delta_y){
    this.x += delta_x;
    this.y += delta_y;
  }

  this.move_pos = function(vector){
    this.x += vector.x;
    this.y += vector.y;
  }

  this.set_int = function(delta_x, delta_y){
    this.x = delta_x;
    this.y = delta_y;
  }
}

function Rectangle(){
  this.pos  = new vector2D();
  this.size = new vector2D();
  this.min_height = 0;

  this.state = 0; // 0 = no change / 1 = Extend_up / 2 = dragging / 3 = Extend_down

  this.collide = function(position){
    if(position.x > this.pos.x && position.x < this.pos.x+this.size.x){
      if(position.y > this.pos.y && position.y < this.pos.y+this.size.y){
        return true;
      }
    }
    return false;
  }

  this.collidePos = function(position){
    if(this.collide(position)){
      return parseInt(((position.y - this.pos.y) / this.size.y) * 20);
    }
    return -1;
  }

  this.set = function(pos_x, pos_y, size_x, size_y){
    this.pos.x = pos_x;
    this.pos.y = pos_y;

    this.size.x = size_x;
    this.size.y = size_y;
  }

  this.extend_up = function(delta_y){
    if(this.pos.y - delta_y < 499/15){
      this.pos.y = 499/15 + 0.5;
      return false;
    }
    if(this.size.y + delta_y >= this.min_height){
      this.pos.y -= delta_y;
      this.size.y += delta_y;
      return true;
    }
  }

  this.extend_down = function(delta_y){
    if(this.pos.y + this.size.y + delta_y > 499){
      this.pos.y = 499 - this.size.y;
      return false;
    }
    if(this.size.y + delta_y >= this.min_height + 2){
      this.size.y += delta_y;
      return true;
    }
  }

  this.move = function(delta_y){
    if(this.pos.y + delta_y < 499/15){
      this.pos.y = 499/15;
      return false;
    }else if(this.pos.y + delta_y + this.size.y > 499){
      this.pos.y = 500-this.size.y;
      return false;
    }
    this.pos.y += delta_y;
    return true;
  }
}

function Schedule(){
  //L M M J V S D
  this.Courses = [false, false, false, false, false, false, false];

  this.schedule_ = [[0, 0],
                    [0, 0],
                    [0, 0],
                    [0, 0],
                    [0, 0],
                    [0, 0],
                    [0, 0]];

  this.rects     = [new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle()]

  this.add       = [new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle()]

  this.dels      = [new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle(),
                    new Rectangle()];

  this.show = function(){
    strokeWeight(0.5);
    stroke(20, 200);
    noFill();
    rect(0, 0, windowSize.x*coefWidth-1, 500);
    for(var x=0;x<nbCols;x++){
      line(x*((windowSize.x*coefWidth)/nbCols), 0, x*((windowSize.x*coefWidth)/nbCols), 499);
    }
    for(var y=7;y<23;y++){
      line(0, (y-7)*499/15, windowSize.x*coefWidth, (y-7)*499/15);
    }
    this.show_layout();
    this.showElems();
  }

  //Reads a schedule entry and transforms it into objects
  this.setSchedule = function(schedule){
    var days = schedule.split(".");

    for(var x=0;x<7;x++){
      var in_day = days[x].split("/");

      if(in_day[0] == "1"){
        this.Courses[x] = true;
        this.schedule_[x] = [parseInt(in_day[1]), parseInt(in_day[2])];
      }
    }

    this.setRects();
  }

  this.setRects = function(){
    for(var x=0;x<7;x++){
      pos_x  = (x+1) * ((windowSize.x*coefWidth)/nbCols);
      pos_y  = (this.schedule_[x][0]-7)*(499/15);
      size_x = ((windowSize.x*coefWidth)/nbCols);
      size_y = (this.schedule_[x][1]-this.schedule_[x][0])*(499/15);
      minimum_h = 2*(499/15) - 1;

      if(this.Courses[x]){
        this.dels[x].set(pos_x + size_x - 17, pos_y + 3, 14, 14);

        this.rects[x].set(pos_x, pos_y, size_x, size_y);
        this.rects[x].min_height = minimum_h;
        if(this.rects[x].size.y < minimum_h){
          this.rects[x].size.y = minimum_h + 1;
          this.schedule_[x][1] = this.schedule_[x][1]+1;
        }
      }
      this.add[x].set(pos_x + size_x/2 - 7, 480, 14, 14);
    }
  }

  //Draws the layout (Big rectangle, days, hours)
  this.show_layout = function(){
    fill(75);
    strokeWeight(0.25);
    textAlign(CENTER);
    textSize(14);
    var days = ["/", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"];
    for(var x=0;x<8;x++){
      text(days[x], x*((windowSize.x*coefWidth)/nbCols) + ((windowSize.x*coefWidth)/nbCols)/2, 499/28);
    }
    for(var h=8;h<23;h++){
      text(str(h)+"h", ((windowSize.x*coefWidth)/nbCols)/2, (h-7)*(499/15) + (499/30));
    }
  }

  this.showAdd = function(){
    for(var y=0;y<7;y++){
      // Draws the + symbol if there's no course and the mouse's in the day rect
      if(parseInt(mouseX/colWidth) == y+1 && !this.Courses[y]){
        fill(0, 255, 0);
        noStroke();
        ellipse(this.add[y].pos.x + this.add[y].size.x/2, this.add[y].pos.y + this.add[y].size.y/2, this.add[y].size.x, this.add[y].size.x);
        noFill();
        stroke(255);
        strokeWeight(1);
        line(this.add[y].pos.x + 3                   , this.add[y].pos.y + this.add[y].size.y/2, this.add[y].pos.x + 11                  , this.add[y].pos.y + this.add[y].size.y/2);
        line(this.add[y].pos.x + this.add[y].size.x/2, this.add[y].pos.y + 3                   , this.add[y].pos.x + this.add[y].size.x/2, this.add[y].pos.y + 11                  );
      }
    }
  }

  //Shows the courses rects
  this.showElems = function(){
    for(var x=0;x<this.Courses.length;x++){
      if(this.Courses[x]){ //If there's something to show at the current day
        //Drawing the back rectangle
        fill(125, 175, 240, 125);
        noStroke();
        rect(this.rects[x].pos.x, this.rects[x].pos.y, this.rects[x].size.x, this.rects[x].size.y);
        //Drawing the front rectangle (noFill)
        stroke(100, 150, 220);
        strokeWeight(2);
        noFill();
        rect(this.rects[x].pos.x, this.rects[x].pos.y, this.rects[x].size.x, this.rects[x].size.y);
        //Calculating position for the text en drawing the text
        pos_y = this.rects[x].pos.y + this.rects[x].size.y/2;
        pos_x = this.rects[x].pos.x + this.rects[x].size.x/2;
        textAlign(CENTER);
        fill(25);
        stroke(25);
        strokeWeight(0.25);
        text(this.schedule_[x][0] + "h - " + this.schedule_[x][1] + "h", pos_x, pos_y);
        //Draws the cross in case mouse is in the rectangle
        if(this.rects[x].collide(new vector2D(mouseX, mouseY))){
          fill(212, 14, 7, 0.74*255);
          noStroke();
          ellipse(this.dels[x].pos.x + this.dels[x].size.x/2, this.dels[x].pos.y + + this.dels[x].size.x/2, this.dels[x].size.x, this.dels[x].size.y);
          stroke(255);
          strokeWeight(1);
          noFill();
          line(this.dels[x].pos.x + 3, this.dels[x].pos.y +  3, this.dels[x].pos.x + 11, this.dels[x].pos.y + 11);
          line(this.dels[x].pos.x + 3, this.dels[x].pos.y + 11, this.dels[x].pos.x + 11, this.dels[x].pos.y + 3);
        }
      }
    }
  }
}

var isMobileUser = mobileAndTabletcheck();

function setup(){
  if(!isMobileUser){
    canvas = createCanvas(coefWidth*windowWidth, 501);
    windowSize = new vector2D(windowWidth, windowHeight);
    for(var x=0;x<scheds.length;x++){
      scheds[x].setRects();
    }

    colWidth = (coefWidth*windowWidth)/nbCols;
  }else{
    var x = users.indexOf(currentUser);
    if(x >= 0){
      document.getElementById("sketch-holder-"+currentUser).innerHTML = "<span style='color:red'>Reconnectez vous plus tard sur pc pour choisir votre horaire</span>";
    }
  }
}

function createSched(username){
  scheds.push(new Schedule());
  users.push(username);

  return users.length-1;
}

function draw(){
  if(!isMobileUser){
    lastMousePos.set_int(mouseX, mouseY);

    fill(255);
    rect(0, 0, windowSize.x, windowSize.y);

    var x = users.indexOf(currentUser);
    canvas.parent("sketch-holder-"+currentUser);

    if(x >= 0){
      scheds[x].show();
      if(mouseY > 0 && mouseY < 500 && mouseX > 0 && mouseX < coefWidth*windowSize.x){
        scheds[x].showAdd();
      }
    }
  }
}

function mousePressed(){
  var x = users.indexOf(currentUser);
  if(x >= 0){
    for(var y=0;y<7;y++){
      var int_pos = scheds[x].rects[y].collidePos(new vector2D(mouseX, mouseY));
      if(int_pos != -1){
        if(int_pos < 3){
          scheds[x].rects[y].state = 1;
        }else if(int_pos < 17){
          scheds[x].rects[y].state = 2;
        }else{
          scheds[x].rects[y].state = 3;
        }
      }else{
        scheds[x].rects[y].state = 0;
      }
    }
  }
}

//Called each time the user releases the mouse
function mouseReleased(){
  var x = users.indexOf(currentUser);
  if(x >= 0){
    for(var y=0;y<7;y++){
      scheds[x].rects[y].state = 0;
      if(scheds[x].dels[y].collide(new vector2D(mouseX, mouseY))){
        scheds[x].Courses[y] = false;
      }
      if(scheds[x].add[y].collide(new vector2D(mouseX, mouseY))){
        if(!scheds[x].Courses[y]){
          scheds[x].Courses[y] = true;
          scheds[x].schedule_[y] = [8, 10];
        }
      }
    }
    scheds[x].setRects();
    mouseMoved();
  }
}

// Sets cursors (Depending on the rects position)
function mouseMoved(){
  var is_on_one = false; // If this stays false, it means the cursor isn't on a rect
  var x = users.indexOf(currentUser);
  if(x >= 0){
    for(var y=0;y<7;y++){
      var int_pos = scheds[x].rects[y].collidePos(new vector2D(mouseX, mouseY));
      if(int_pos != -1){
        if(int_pos < 3){
          cursor('row-resize');
        }else if(int_pos < 17){
          cursor('grab');
        }else{
          cursor('row-resize');
        }
        is_on_one = true;
        if(scheds[x].dels[y].collide(new vector2D(mouseX, mouseY))){
          cursor(ARROW);
        }
      }
    }
    if(!is_on_one){
      cursor(ARROW);
    }
  }
}

// Either moves, extends up or down a rect
function mouseDragged(){
  cursor('grabbing');
  var x = users.indexOf(currentUser);
  if(x >= 0){
    for(var y=0;y<7;y++){
      if(scheds[x].rects[y].state == 1){
        if(scheds[x].rects[y].extend_up(lastMousePos.y - mouseY)){
          scheds[x].dels[y].pos.y -= lastMousePos.y - mouseY;
        }
        scheds[x].schedule_[y][0] = parseInt(scheds[x].rects[y].pos.y / (499/15)) + 7;
        scheds[x].schedule_[y][1] = parseInt((scheds[x].rects[y].pos.y + scheds[x].rects[y].size.y) / (499/15)) + 7;
      }else if(scheds[x].rects[y].state == 2){
        if(scheds[x].rects[y].move(mouseY - lastMousePos.y)){
          scheds[x].dels[y].pos.y -= lastMousePos.y - mouseY;
        }
        scheds[x].schedule_[y][0] = parseInt(scheds[x].rects[y].pos.y / (499/15)) + 7;
        scheds[x].schedule_[y][1] = parseInt((scheds[x].rects[y].pos.y + scheds[x].rects[y].size.y) / (499/15)) + 7;
      }else if(scheds[x].rects[y].state == 3){
        scheds[x].rects[y].extend_down(mouseY - lastMousePos.y);
        scheds[x].schedule_[y][0] = parseInt(scheds[x].rects[y].pos.y / (499/15)) + 7;
        scheds[x].schedule_[y][1] = parseInt((scheds[x].rects[y].pos.y + scheds[x].rects[y].size.y) / (499/15)) + 7;
      }
    }
  }
}

//Transforms the objects from the schedule into Html Form
function setHtmlForm(){
  var usr = users.indexOf(currentUser);
  if(usr >= 0){
    divider = document.getElementById("sketch-holder-" + currentUser);
    formHTML = "<div style=\"display:none;\">";

    if(!isMobileUser){
      formHTML += "\n<input type=\"checkbox\" id=\"isMobileUser\" name=\"isMobileUser\">";
      days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
      for(var x=0;x<7;x++){
        if(scheds[usr].Courses[x]){
          formHTML += "\n<input type=\"checkbox\" id=\"" + days[x] + "\"      name=\"course " + days[x] + "\" checked>";
          formHTML += "\n<input type=\"number\"   id=\"" + days[x] + "Start\" name=\""       + days[x] + "Start\" value=\"" + scheds[usr].schedule_[x][0] + "\">";
          formHTML += "\n<input type=\"number\"   id=\"" + days[x] + "End\"   name=\""       + days[x] + "End\" value=\"" + scheds[usr].schedule_[x][1] + "\">";
        }else{
          formHTML += "\n<input type=\"checkbox\" id=\"" + days[x] + "\"      name=\"course" + days[x] + "\">";
        }
      }
    }else{
      formHTML += "\n<input type=\"checkbox\" id=\"isMobileUser\" name=\"isMobileUser\" checked>";
    }
    formHTML += "\n</div>";
    divider.innerHTML = formHTML;
  }
}
