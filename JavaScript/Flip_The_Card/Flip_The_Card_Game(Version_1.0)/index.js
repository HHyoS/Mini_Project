const cardArray = [
  {
    name: "bird",
    img: "./imgs/bird.png",
    id: null,
  },
  {
    name: "bird",
    img: "./imgs/bird.png",
    id: null,
  },
  {
    name: "cat",
    img: "./imgs/cat.png",
    id: null,
  },
  {
    name: "cat",
    img: "./imgs/cat.png",
    id: null,
  },
  {
    name: "crocodil",
    img: "./imgs/crocodil.png",
    id: null,
  },
  {
    name: "crocodil",
    img: "./imgs/crocodil.png",
    id: null,
  },
  {
    name: "dog",
    img: "./imgs/dog.png",
    id: null,
  },
  {
    name: "dog",
    img: "./imgs/dog.png",
    id: null,
  },
  {
    name: "igoana",
    img: "./imgs/igoana.png",
    id: null,
  },
  {
    name: "igoana",
    img: "./imgs/igoana.png",
    id: null,
  },
  {
    name: "wolf",
    img: "./imgs/wolf.png",
    id: null,
  },
  {
    name: "wolf",
    img: "./imgs/wolf.png",
    id: null,
  },
];

let clickFirst = -1;
let clickSecond = -1;
let clickCount = 0;
const gameDom = [];

const getGameDOM = () => {
  const rows = document.querySelectorAll(".row"); // ㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏㅏ
  //row의 타입은 NodeList

  for (let a = 0; a < rows.length; ++a) {
    gameDom[a] = rows[a].querySelectorAll(".column");
  }
};

cardArray.sort(() => 0.5 - Math.random());
const setIDtoCardArray = () => {
  cardArray[0].id = "0-0";
  cardArray[1].id = "0-1";
  cardArray[2].id = "0-2";
  cardArray[3].id = "0-3";
  cardArray[4].id = "1-0";
  cardArray[5].id = "1-1";
  cardArray[6].id = "1-2";
  cardArray[7].id = "1-3";
  cardArray[8].id = "2-0";
  cardArray[9].id = "2-1";
  cardArray[10].id = "2-2";
  cardArray[11].id = "2-3";
};

const setClickHistory = (location) => {
  if(clickFirst === -1){
    clickFirst = location;
  }
  else{
    if(location != clickFirst)
      clickSecond = location;
    else
      clickCount -= 1;
  }
};

const createBoard = () => {
  for (let i = 0; i < gameDom.length; ++i) {
    for (let j = 0; j < gameDom[i].length; ++j) {
      const card = document.createElement("img");
      card.setAttribute("src", "./imgs/question.png");
      gameDom[i][j].appendChild(card);
    }
  }
};

const backFilp = () => {
  const paredIdFirst = cardArray[clickFirst].id.split("-");
  const paredIdSecond = cardArray[clickSecond].id.split("-");
  setTimeout(()=>{
    gameDom[paredIdFirst[0]][paredIdFirst[1]].querySelector("img").src="./imgs/question.png";
    gameDom[paredIdSecond[0]][paredIdSecond[1]].querySelector("img").src="./imgs/question.png";
    
  },500)
  
}

const isCorrect = () => {
  if(cardArray[clickFirst].name === cardArray[clickSecond].name){
    cardArray[clickFirst].done = true;
    cardArray[clickSecond].done = true;
  }
  else{
    backFilp();
  }
}
const flip = (location) => {
  if(!cardArray[location].done){
    setClickHistory(location);

    const parsedId = cardArray[location].id.split("-");
    gameDom[parsedId[0]][parsedId[1]].querySelector("img").src=cardArray[location].img;

    clickCount++;
    if(clickCount ===2){
      clickCount =0;
      isCorrect();
    }

    console.log(clickCount);
    if(clickFirst !== -1 && clickSecond !== -1){
      clickFirst= -1;
      clickSecond = -1;
    }
  }
};



getGameDOM();
setIDtoCardArray();
createBoard();
