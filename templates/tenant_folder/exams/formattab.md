
<div class="parent">
    <div class="div1">1</div>
    <div class="div2">2</div>
    <div class="div3">3</div>
    <div class="div4">4</div> <!-- Type de note 1-->
    <div class="div5">5</div> <!-- sous Type de note 1.1-->
    <div class="div6">6</div> <!-- sous Type de note 1.2-->
    <div class="div7">7</div> <!-- sous Type de note 1.4-->
    <div class="div8">8</div>
    <div class="div9">9</div>
    <div class="div10">10</div>
    <div class="div11">11</div>
    <div class="div12">12</div>
    <div class="div13">13</div>
    <div class="div14">14</div>
    <div class="div16">16</div>
    <div class="div17">17</div>
    <div class="div18">18</div>
    <div class="div19">19</div>
    <div class="div20">20</div>
    <div class="div21">21</div>
    <div class="div22">22</div>
    <div class="div23">23</div>
    <div class="div24">24</div>
    <div class="div25">25</div>
    <div class="div26">26</div>
    <div class="div27">27</div>
</div>
    


.parent {
    display: grid;
    grid-template-columns: repeat(12, 1fr);
    grid-template-rows: repeat(5, 1fr);
    gap: 0px;
}
    
.div1 {
    grid-row: span 2 / span 2;
}

.div2 {
    grid-row: span 2 / span 2;
}

.div3 {
    grid-row: span 2 / span 2;
}

.div4 {
    grid-column: span 3 / span 3;
}

.div5 {
    grid-column-start: 4;
    grid-row-start: 2;
}

.div6 {
    grid-column-start: 5;
    grid-row-start: 2;
}

.div7 {
    grid-column-start: 6;
    grid-row-start: 2;
}

.div8 {
    grid-column: span 3 / span 3;
    grid-column-start: 7;
    grid-row-start: 1;
}

.div9 {
    grid-column-start: 7;
    grid-row-start: 2;
}

.div10 {
    grid-column-start: 8;
    grid-row-start: 2;
}

.div11 {
    grid-column-start: 9;
    grid-row-start: 2;
}

.div12 {
    grid-row: span 2 / span 2;
    grid-column-start: 10;
    grid-row-start: 1;
}

.div13 {
    grid-row: span 2 / span 2;
    grid-column-start: 11;
    grid-row-start: 1;
}

.div14 {
    grid-row: span 2 / span 2;
    grid-column-start: 12;
    grid-row-start: 1;
}

.div16 {
    grid-row-start: 3;
}

.div17 {
    grid-row-start: 3;
}

.div18 {
    grid-row-start: 3;
}

.div19 {
    grid-row-start: 3;
}

.div20 {
    grid-row-start: 3;
}

.div21 {
    grid-row-start: 3;
}

.div22 {
    grid-row-start: 3;
}

.div23 {
    grid-row-start: 3;
}

.div24 {
    grid-row-start: 3;
}

.div25 {
    grid-row-start: 3;
}

.div26 {
    grid-row-start: 3;
}

.div27 {
    grid-row-start: 3;
}
        