
let url = new URL(window.location.href.toString())
let columns = parseInt(url.searchParams.get("columns")) || 3
let rows = parseInt(url.searchParams.get("rows")) || 3
let protivAI = url.searchParams.get("AI") == "true"
let player1 = url.searchParams.get("player1")
let player2 = url.searchParams.get("player2")
let dubina1 = parseInt(url.searchParams.get("depth1"))
let dubina2 = parseInt(url.searchParams.get("depth2"))
let obavestenje = document.getElementById("obavestenje")
let h1 = document.createElement("h1")
let log = document.getElementById("log")


// Globalne varijable koje pamte trenutno stanje igre i neke pomocne vrednosti
let brojacCrtica = 0
let brojacPolja = 0
let naPotezu = 0
let krajIgre = false
let dozvola = true
let scoreCrveni = 0
let scorePlavi = 0
let osvojioPolje = false

let crveni = document.getElementById("crveni")
let plavi = document.getElementById("plavi")
let span1 = document.getElementById("span1")
let span2 = document.getElementById("span2")
let span3 = document.getElementById("span3")


function tabela() {
   // table u html-u 
   let table = document.getElementById("game")
   table.innerHTML = ""
   brojacCrtica = 0
   brojacPolja = 0
   naPotezu = 0
   krajIgre = false
   dozvola = true
   scoreCrveni = 0
   scorePlavi = 0
   span1.innerHTML = 0
   span2.innerHTML = 0
   span3.innerHTML = "Crveni igrac"
   log.innerHTML = ""





   for (let i = 0; i < rows * 2 + 1; i++) {
      tr = document.createElement("tr")
      tr.style.height = i % 2 == 0 ? "20px" : "auto"

      for (let j = 0; j < columns * 2 + 1; j++) {
         let td = document.createElement("td")
         td.style.width = j % 2 == 0 ? "20px" : "auto"

         if (i % 2 == 0 && j % 2 == 0)

            td.style.backgroundColor = "grey"
         else if (i % 2 == 1 && j % 2 == 1) {

            td.style.backgroundColor = "lightgrey"
            td.id = td.innerHTML = "p" + brojacPolja++
         }
         else {

            td.style.backgroundColor = "white"
            td.id = td.innerHTML = brojacCrtica++



            td.onclick = function () {
               if (dozvola)
                  izvrsiPotez(parseInt(td.id))
               else {
                  alert("Cekamo odgovor od ai-a")
               }
            }
         }
         // td/celiju koju smo kreirali dodajemo u tr/row
         tr.appendChild(td)
      }

      // i taj novi tr/row dodajemo u tabelu
      table.appendChild(tr)


   }
   if (player1 != "player") {
      let random = Math.floor(Math.random() * 23)
      izvrsiPotez(random)
   }
}
function download() {
   text = document.getElementById("log").innerHTML
   text = text.replaceAll("<br>", "\n")
   text = "Kolone " + columns + " \n" + "Redovi " + rows + "\n" + text
   var element = document.createElement('a');
   element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
   element.setAttribute('download', "log.txt");

   element.style.display = 'none';
   document.body.appendChild(element);

   element.click();

   document.body.removeChild(element);
}
if (naPotezu == 0)
   span3.innerHTML = "Crveni igrac"
else
   span3.innerHTML = "Plavi igrac"


tabela()




function readTextFile(file) {
   var rawFile = new XMLHttpRequest();
   rawFile.open("GET", file, false);
   rawFile.onreadystatechange = function () {
      if (rawFile.readyState === 4) {
         if (rawFile.status === 200 || rawFile.status == 0) {


            var potez = rawFile.responseText;
            var potezi = []
            var kolone = rawFile.responseText;
            var redovi = rawFile.responseText;
            var sviPotezi = potez.split("\n")
            duzina = sviPotezi.length
            kolone = kolone.split(" ")[1]
            redovi = redovi.split(" ")[3]
            //console.log(sviPotezi)
            //console.log(kolone)
            //console.log(redovi)
            var i = 0
            var index = 1
            sviPotezi.forEach(pokusaji => {
               potezi[i] = pokusaji.split(" ")[1],
                  index = index + 2,
                  console.log(potezi[i]),
                  i++
            });

            columns = parseInt(potezi[0])
            rows = parseInt(potezi[1])
            var delay = 1000
            for (var i = 2; i < potezi.length; i++) {
               //setInterval(() => izvrsiPotez(parseInt(potezi[i])) , 2000)
               izvrsiPotez(parseInt(potezi[i]))

            }
         }
      }
   }
   rawFile.send(null);
}

let input = document.querySelector('input')
if (input) {
   input.addEventListener('change', () => {
      let files = input.files;

      if (files.length == 0) return;


      var file = files[0];



      let reader = new FileReader();

      reader.onload = (e) => {
         const file = e.target.result;


         var lines = file.split("\n");
         var duzina = lines.length
         var i = 0;
         var potezi = []
         for (let i = 0; i < duzina - 1; i++) {
            potezi[i] = lines[i].split(" ")[1]
            console.log(potezi[i])
         }


         columns = parseInt(potezi[0])
         rows = parseInt(potezi[1])
         tabela()
         for (var i = 2; i < duzina - 1; i++) {
            izvrsiPotez(parseInt(potezi[i]))
         }
         //textarea.value = lines.join('\n'); 
         // console.log(file2)
      };

      reader.onerror = (e) => alert(e.target.error.name);

      reader.readAsText(file);
   });
}

//let tekst = " "
function izvrsiPotez(potez) {

   // Ako je kraj igre onda prekini dalje izvrsavanje ove funkcije
   if (krajIgre)
      return


   const crtica = document.getElementById(potez)

   if (crtica.style.backgroundColor == "tomato" || crtica.style.backgroundColor == "skyblue")
      return

   // Oboji to polje u zavisnosti od toga ko je na potezu
   crtica.style.backgroundColor = naPotezu == 0 ? "tomato" : "skyblue"


   osvojioPolje = false
   tekst = " "
   for (let i = 0; i < brojacPolja; i++) {
      const polje = document.getElementById("p" + i)
      if (polje.style.backgroundColor == "lightgrey") {
         if (osvojenoPoljeSaIndeksom(i)) {
            polje.style.backgroundColor = naPotezu == 0 ? "tomato" : "skyblue"

            if (naPotezu == 0)
               scoreCrveni++


            else
               scorePlavi++
            span1.innerHTML = scoreCrveni
            span2.innerHTML = scorePlavi

            osvojioPolje = true
            if (osvojioPolje)
               tekst = " , i osvojio je polje p" + i + "!"

         }

      }

   }



   if (naPotezu == 0)
      log.innerHTML += "Potez " + potez + " : Je odigrao crveni igrac" + tekst + "<br>"

   else
      log.innerHTML += "Potez " + potez + " : Je odigrao plavi igrac" + tekst + "<br>"





   if (!osvojioPolje)
      naPotezu = 1 - naPotezu

   // Proveri da li je kraj igre
   gameover()

   if (player2 == "aieasy" && naPotezu == 1) {
      let stanjeCrtica = trenutnoStanjeCrtica()
      let stanjePolja = trenutnoStanjePolja()
      let slanje = `http://localhost:8000/ai?crtice=${stanjeCrtica}&polja=${stanjePolja}&player=1&tezina=easy&columns=${columns}&dubina=${0}`
      p = document.createElement('p')
      dozvola = false
      Fetch(slanje)
   }

   // Ako smo izabrali da igramo protiv AI onda uzimamo potez koji treba odigrati od AI
   else if (player2 == "aimedium" && naPotezu === 1) {

      let stanjeCrtica = trenutnoStanjeCrtica()
      let stanjePolja = trenutnoStanjePolja()
      let slanje = `http://localhost:8000/ai?crtice=${stanjeCrtica}&polja=${stanjePolja}&player=1&tezina=medium&columns=${columns}&dubina=${dubina2}`
      p = document.createElement('p')
      dozvola = false
      Fetch(slanje)


   }
   else if (player1 == "aimedium" && naPotezu == 0) {
      let stanjeCrtica = trenutnoStanjeCrtica()
      let stanjePolja = trenutnoStanjePolja()
      let slanje = `http://localhost:8000/ai?crtice=${stanjeCrtica}&polja=${stanjePolja}&player=1&tezina=medium&columns=${columns}&dubina=${dubina1}`
      p = document.createElement('p')
      dozvola = false
      Fetch(slanje)
   }
   else if (player1 == "aieasy" && naPotezu == 0) {
      let stanjeCrtica = trenutnoStanjeCrtica()
      let stanjePolja = trenutnoStanjePolja()
      let slanje = `http://localhost:8000/ai?crtice=${stanjeCrtica}&polja=${stanjePolja}&player=1&tezina=easy&columns=${columns}&dubina=${0}`
      p = document.createElement('p')
      dozvola = false
      Fetch(slanje)
   }
   else if (player2 == "aihard" && naPotezu == 1) {
      let stanjeCrtica = trenutnoStanjeCrtica()
      let stanjePolja = trenutnoStanjePolja()
      let slanje = `http://localhost:8000/ai?crtice=${stanjeCrtica}&polja=${stanjePolja}&player=1&tezina=hard&columns=${columns}&dubina=${dubina2}`
      p = document.createElement('p')
      dozvola = false
      Fetch(slanje)
      
   }
   else if (player1 == "aihard" && naPotezu == 0) {
      let stanjeCrtica = trenutnoStanjeCrtica()
      let stanjePolja = trenutnoStanjePolja()
      let slanje = `http://localhost:8000/ai?crtice=${stanjeCrtica}&polja=${stanjePolja}&player=1&tezina=hard&columns=${columns}&dubina=${dubina1}`
      p = document.createElement('p')
      dozvola = false
      Fetch(slanje)

   }

   if (naPotezu == 0)
      span3.innerHTML = "Crveni igrac"
   else
      span3.innerHTML = "Plavi igrac"


}
function Fetch(slanje) {

   fetch(slanje, { mode: 'cors' })
      .then(function (response) {
         if (response.ok) {
            //dozvola = false
            return response.text()
         }
         

      })
      .then(function (data) {
         if (data) {
            izvrsiPotez(data)
            if(osvojioPolje)
               dozvola = false
            else
               dozvola = true   
         }
         //else
         //dozvola = true
      });
}


function osvojenoPoljeSaIndeksom(indeksPolja) {

   const idCrticeIznad = Math.floor(indeksPolja / columns) * (columns + 1) + indeksPolja

   const indeksi = [idCrticeIznad, idCrticeIznad + columns, idCrticeIznad + columns + 1, idCrticeIznad + 2 * columns + 1]

   for (let i = 0; i < 4; i++) {
      crtica = document.getElementById(indeksi[i])

      if (crtica.style.backgroundColor === "white")
         return false

   }

   return true
}


function trenutnoStanjeCrtica() {
   let stanje = ""
   for (let i = 0; i < brojacCrtica; i++) {
      let crtica = document.getElementById(i.toString())
      switch (crtica.style.backgroundColor) {
         case "tomato":
            stanje += "0"
            break;
         case "skyblue":
            stanje += "1"
            break;
         default:
            stanje += "2"
            break;
      }
   }

   return stanje
}

// Vraca string koji predstavlja trenutno stanje polje, obilazi sva polja i kreira string na osnovu boje polja
function trenutnoStanjePolja() {
   let stanje = ""
   for (let i = 0; i < brojacPolja; i++) {
      let polje = document.getElementById("p" + i.toString())
      switch (polje.style.backgroundColor) {
         case "tomato":
            stanje += "0"
            break;
         case "skyblue":
            stanje += "1"
            break;
         default:
            stanje += "2"
            break;
      }
   }

   return stanje
}

// Proverava da li je gameover
function gameover() {

   const stanje = trenutnoStanjePolja().includes("2")
   if (stanje === false) { // Ako je kraj igre
      krajIgre = true

      // Izbroji koliko polja je osovjio igrac '0'
      let brojNula = 0
      let stanjePolja = trenutnoStanjePolja()
      for (let i = 0; i < stanjePolja.length; i++)
         if (stanjePolja[i] == "0")
            brojNula++

      // Ako je osvojio vise od polovine ukupnog broja polja onda je pobedio 0
      if (brojNula > brojacPolja / 2)
         alert("Pobedio je crveni igrac!")
      // Ako je broj osvojienih polja jednak polovini broja polja onda je nereseno
      else if (brojNula === brojacPolja / 2)
         alert("Nereseno!")
      // Inace je pobedio igrac broj '1' tj. plavi igrac
      else
         alert("Pobedio je plavi igrac!")
   }

}