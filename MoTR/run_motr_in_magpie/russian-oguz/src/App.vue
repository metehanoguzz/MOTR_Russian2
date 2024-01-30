<!-- Window is fixed, 102px, pointer cursor, more gradual blurry effect on surrounding words. -->
<!--  Comprehension questions appear afterwards in the same slide -->

<template>
  <!-- disabled translation -->
  <Experiment title="Russian MoTR Study" translate="no">
    <Screen :title="'Добро пожаловать'" class="instructions" :validations="{
        SubjectID: {
          minLength: $magpie.v.minLength(2)
        }
      }">
        <!-- <WelcomeScreen /> -->
        <div style="width: 40em; margin: auto;">

          <div style="background-color: lightgrey; padding: 10px;">
              <b> Университет Южной Калифорнии: Информация</b>
          </div>
          <p>
            Здравствуйте! Меня зовут Зузанна Фукс, я профессор Университета Южной Калифорнии в Лос-Анджелесе. 
            <br><br>
            В круг моих исследований входит изучение того, как люди читают по-русски. Конкретное исследование, в котором, как я надеюсь, вы согласитесь поучаствовать, называется «Вопросы русского согласования».
            <br><br>
            Ваше участие в этом исследование носит добровольный характер, и в любой момент работы я буду рада вашим вопросам или уточнениям.
            <br><br>
            Вы можете стать участником исследования, если вы отвечаете следующим критериям:
            <br><br>
            1.	Вы выросли в России и жили там первые 18 лет вашей жизни.<br>
            2.	Если вы сейчас находитесь за пределами России, вы выехали оттуда после 2021 г.<br>
            3.	Вам от 18 до 35 лет. 
            <br><br>
            Если вы согласитесь принять участие в исследовании, вам нужно будет в течение 10-12 минут читать по-русски и отвечать на вопросы по чтению.
            <br><br>
            По завершении теста вы получите компенсацию в сумме 4 долларов США на платформе Prolific.
            <br><br>
            Результаты исследования будут докладываться на научных конференциях и включаться в журнальные публикации. Ваши личные данные нигде не будут указаны. Конфиденциальность ваших личных данных будет строго соблюдаться, и до публикации или докладов они будут анонимизированы. Анонимизированные данные могут в дальнейшем быть использованы и другими учеными.   
            <br><br>
            Если у вас есть вопросы по исследованию, пожалуйста, свяжитесь со мной по электронной почте:
            zfuchs@usc.edu. С вопросами о ваших правах как участника экспериментов, вы также можете обратиться в Комитет по этике Университета Южной Калифорнии: (323) 442-0114 (тел.), hrpp@usc.edu (эл. почта). 
            <br>
          </p>
          <br>
        </div>
        <tr>
          <!-- Explain TurkID -->
          <td>Пожалуйста, введите свой идентификатор работника, чтобы продолжить:&nbsp</td><td><input name="TurkID" type="text" class="obligatory" v-model="$magpie.measurements.SubjectID"/></td>
        </tr>
        <div v-if="
            $magpie.measurements.SubjectID&&
            !$magpie.validateMeasurements.SubjectID.$invalid 
            ">
          <br> Нажимая кнопку ниже, вы соглашаетесь на участие в этом исследовании: <br><br>
          <br />
          <button 
            @click=" $magpie.addExpData({ SubjectId: $magpie.measurements.SubjectID}); $magpie.nextScreen()">
            Продолжить
          </button>
          
        </div>
    </Screen>

    <Screen class="instructions">
        <div style="width: 40em; margin: auto;">
          <div style="background-color: lightgrey; padding: 10px;">
              <b>Инструкции</b>
          </div>
          <br>
          <p>В этом исследовании вы будете читать короткие тексты и отвечать на вопросы по ним. Однако, в отличие от обычного чтения, тексты будут размыты. 
            Чтобы сделать текст четким, наведите на него курсор мышки. Уделите чтению текста столько времени, сколько вам необходимо для его понимания. 
            Когда вы закончите читать текст, ответьте на вопрос, расположенный внизу экрана, и нажмите «Далее», чтобы продолжить.</p>   
          
          <p>Чтобы привыкнуть к тому, как устроено исследование, перед началом основного исследования вы выполните несколько тренировочных заданий.</p> 
          <br>
       </div>
      <button style="transform: translate(-50%, -50%)" @click="$magpie.nextScreen()">
        Начать практику
      </button>
    </Screen>

    <template v-for="(trial, i) of practice_trials">
      <Screen :key="i" class="main_screen" :progress="i / practice_trials.length">
        <Slide>
          <form>
            <input type="hidden" class="item_id" :value="trial.item_id">
            <input type="hidden" class="type_id" :value="trial.type_id">
            <input type="hidden" class="condition" :value="trial.condition">
            <input type="hidden" class="list" :value="trial.list">
          </form>
          <div class="oval-cursor"></div>
          <template>
            <div v-if="showFirstDiv" class="readingText" @mousemove="moveCursor" @mouseleave="changeBack">
              <template v-for="(word, index) of trial.text.split(' ')">
                <span :key="index" :data-index="index" >
                  {{ word }}
                </span>
              </template>
            </div>
            <div class="blurry-layer" style="opacity: 0.3; filter: blur(3.5px); transition: all 0.3s linear 0s;"> 
              {{trial.text}}
            </div>
          </template>
          <button v-if="showFirstDiv" style= "bottom:50%; transform: translate(-50%, -50%)" @click="trial.question !== null ? toggleDivs(): saveAndDisable()" :disabled="!hasRead">
            {{ trial.question !== null ? 'Продолжить' : 'Продолжить' }}
          </button>

          <div v-else style = "position:absolute; bottom:15%; text-align: center; width: 100%; min-width: -webkit-fill-available;" >
            <template>
              <form>
                <!-- comprehension questions and the response options -->
                <!-- <div>{{ trial.question ? trial.question.replace(/ ?["]+/g, '') : '' }}</div> -->
                <div>{{ trial.question }}</div>
                <template v-for='(word, index) of trial.response_options'>
                  <input :id="'opt_'+index" type="radio" :value="word" name="opt" v-model="$magpie.measurements.response"/>{{ word }}<br/>
                    <!-- <label :for="'opt_'+index"> {{ word }}&nbsp</label> -->
                </template>
              </form>
            </template>
          </div>
          
          <button v-if="$magpie.measurements.response" style="transform: translate(-50%, -50%)" @click="toggleDivs(); $magpie.saveAndNextScreen()">
            Продолжить
          </button>
        </Slide>
      </Screen>
    </template>
    
    <Screen :title="'Практика закончена'" class="instructions">
      <p>Вы закончили тренировку! Теперь можно перейти к основному исследованию.</p> 
      <p>Пожалуйста, нажмите кнопку ниже, чтобы начать.</p>
      <button style="transform: translate(-50%, -50%)" @click=" $magpie.nextScreen()">
            Продолжить
      </button>
    </Screen>

    <template v-for="(trial, i) of trials">
      <Screen :key="i" class="main_screen" :progress="i / trials.length">
        <Slide>
          <form>
            <input type="hidden" class="item_id" :value="trial.item_id">
            <input type="hidden" class="type_id" :value="trial.type_id">
            <input type="hidden" class="condition" :value="trial.condition">
            <input type="hidden" class="list" :value="trial.list">
          </form>
          <div class="oval-cursor"></div>
          <template>
            <div v-if="showFirstDiv" class="readingText" @mousemove="moveCursor" @mouseleave="changeBack">
              <template v-for="(word, index) of trial.text.split(' ')">
                <span :key="index" :data-index="index" >
                  {{ word }}
                </span>
              </template>
            </div>
            <div class="blurry-layer" style="opacity: 0.3; filter: blur(3.5px); transition: all 0.3s linear 0s;"> 
              {{trial.text}}
            </div>
          </template>
          <button v-if="showFirstDiv" style= "bottom:50%; transform: translate(-50%, -50%)" @click="trial.question !== null ? toggleDivs(): saveAndDisable()" :disabled="!hasRead">
            {{ trial.question !== null ? 'Продолжить' : 'Продолжить' }}
          </button>

          <div v-else style = "position:absolute; bottom:15%; text-align: center; width: 100%; min-width: -webkit-fill-available;" >
            <template>
              <form>
                <!-- comprehension questions and the response options -->
                <!-- <div>{{ trial.question ? trial.question.replace(/ ?["]+/g, '') : '' }}</div> -->
                <div>{{ trial.question }}</div>
                <template v-for='(word, index) of trial.response_options'>
                  <input :id="'opt_'+index" type="radio" :value="word" name="opt" v-model="$magpie.measurements.response"/>{{ word }}<br/>
                    <!-- <label :for="'opt_'+index"> {{ word }}&nbsp</label> -->
                </template>
              </form>
            </template>
          </div>
          
          <button v-if="$magpie.measurements.response" style="transform: translate(-50%, -50%)" @click="toggleDivs(); $magpie.saveAndNextScreen()">
            Продолжить
          </button>
        </Slide>
      </Screen>

    </template>

    <Screen style="min-height: 700px;">
      <div style="background-color: lightgrey; padding: 10px; width: 650px;">
            <b> демографическая информация </b>
      </div>
    
      <p>1. В данный момент я живу в русскоговорящей стране. &nbsp</p>
      <MultipleChoiceInput
          :response.sync= "$magpie.measurements.russianCountry"
          orientation="horizontal"
          :options="['Да', 'Нет']" />
      <p v-if = "$magpie.measurements.russianCountry == 'Нет'"> Как долго вы проживаете в нерусскоязычной стране? &nbsp </p>
      <TextareaInput v-if = "$magpie.measurements.russianCountry == 'Нет'"
            :response.sync= "$magpie.measurements.russianCountry2"
      />
      <br>
      <p>2. Я использую _____.</p>
        <MultipleChoiceInput
            :response.sync= "$magpie.measurements.device"
            orientation="horizontal"
            :options="['Компьютерную мышку', 'Трекпад', 'другое' ]" />
        <p v-if = "$magpie.measurements.device == 'другое'">Если вы указали другое, пожалуйста уточните: &nbsp &nbsp</p>
        <TextareaInput v-if = "$magpie.measurements.device == 'другое'"
              :response.sync= "$magpie.measurements.otherDevice"
        />
        <br>
      <p>3. Я _____. &nbsp</p>
        <MultipleChoiceInput
            :response.sync= "$magpie.measurements.hand"
            orientation="horizontal"
            :options="['Левша', 'Правша', 'Амбидекстр']" />
      <button style= "bottom:0%; transform: translate(-50%, -50%)" @click="$magpie.saveAndNextScreen();">Submit</button>
    </Screen>

    <SubmitResultsScreen />
  </Experiment>
</template>

<script>
// Load data from csv files as javascript arrays with objects
import russ_list1 from '../trials/Russ_MoTR_List4.tsv';
import russ_list2 from '../trials/Russ_MoTR_List4.tsv';
import russ_list3 from '../trials/Russ_MoTR_List4.tsv';
import russ_list4 from '../trials/Russ_MoTR_List4.tsv';
import russ_practice from '../trials/Russ_MoTR_List_Practice.tsv';

import _ from 'lodash';
export default {
  name: 'App',
  data() {
    const lists = [russ_list1, russ_list2, russ_list3, russ_list4];
    const chosenItems = lists[Math.floor(Math.random() * lists.length)]; // randomly choose one of the lists
    const shuffledItems = _.shuffle(chosenItems); 
    const practice_trials = russ_practice ;
    const trials = shuffledItems;
    // Create a new column in localCoherences called 'response_options'
    // that concatenates the word in response_true with the two words in response_distractors
    const updatedTrials = trials.map(trial => {
      return {
        ...trial,
        response_options: _.shuffle(`${trial.response_true}|${trial.response_distractors}`.replace(/ ?["]+/g, "").split("|")),
      }
    });
    const updatedPracticeTrials = practice_trials.map(trial => {
      return {
        ...trial,
        response_options: _.shuffle(`${trial.response_true}|${trial.response_distractors}`.replace(/ ?["]+/g, "").split("|")),
      }
    });
    return {
      hasRead: false,
      trials: updatedTrials,
      practice_trials: updatedPracticeTrials,
      currentIndex: null,
      showFirstDiv: true,
      // currentItem: null,
      mousePosition: {
          x: 0,
          y: 0,
        },
  }},
  computed: {
  },
  mounted() { 
    setInterval(this.saveData, 50);
    },
  methods: {
    changeBack() {
      this.$el.querySelector(".oval-cursor").classList.remove('grow');
      this.$el.querySelector(".oval-cursor").classList.remove('blank');
      this.currentIndex = null;
    },
    saveData() {
        if (this.currentIndex !== null) {
          const currentElement = this.$el.querySelector(`span[data-index="${this.currentIndex}"]`);
          if (currentElement) {
            // console.log('word: ', currentElement.innerHTML);
            $magpie.addTrialData({
              Type: this.$el.querySelector(".type_id").value,
              Condition: this.$el.querySelector(".condition").value,
              ItemId: this.$el.querySelector(".item_id").value,
              List: this.$el.querySelector(".list").value,
              Index: this.currentIndex,
              Word: currentElement.innerHTML,
              mousePositionX: this.mousePosition.x,
              mousePositionY: this.mousePosition.y,
              wordPositionTop: currentElement.offsetTop,
              wordPositionLeft: currentElement.offsetLeft,
              wordPositionBottom: currentElement.offsetHeight + currentElement.offsetTop,
              wordPositionRight: currentElement.offsetWidth + currentElement.offsetLeft
          });
        } else {
          $magpie.addTrialData({
              Type: this.$el.querySelector(".type_id").value,
              Condition: this.$el.querySelector(".condition").value,
              ItemId: this.$el.querySelector(".item_id").value,
              List: this.$el.querySelector(".list").value,
              Index: this.currentIndex,
              mousePositionX: this.mousePosition.x,
              mousePositionY: this.mousePosition.y,
          });
          
        }
      }},
    moveCursor(e) {
      this.hasRead = true;
      this.$el.querySelector(".oval-cursor").classList.add('grow');
      let x = e.clientX;
      let y = e.clientY;
      const elementAtCursor= document.elementFromPoint(x, y).closest('span');
      if (elementAtCursor){
        this.$el.querySelector(".oval-cursor").classList.remove('blank');
        this.currentIndex = elementAtCursor.getAttribute('data-index');
      } else {
        this.$el.querySelector(".oval-cursor").classList.add('blank');
        const elementAboveCursor = document.elementFromPoint(x, y-10).closest('span');
        if (elementAboveCursor){
          this.currentIndex = elementAboveCursor.getAttribute('data-index');
        } else {
          this.currentIndex = -1;
        }
      }
      
      this.$el.querySelector(".oval-cursor").style.left = `${x+12}px`;
      this.$el.querySelector(".oval-cursor").style.top = `${y-6}px`;
      this.mousePosition.x = e.offsetX;
      this.mousePosition.y = e.offsetY;
    },
    toggleDivs() {
    this.showFirstDiv = !this.showFirstDiv;
    this.hasRead = false;
    },

    saveAndDisable() {
    $magpie.saveAndNextScreen();
    this.hasRead = false;
    },

    getScreenDimensions() {
      return {
        window_inner_width: window.innerWidth,
        window_inner_height: window.innerHeight
      };
    }
  },
};
</script>


<style>
  .experiment {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .main_screen {
    isolation: isolate;
    position: relative;
    width: 100%;
    height: auto;
    font-size: 18px;
    line-height: 40px;
  }
  .debugResults{
    width: 100%;
  }
  .readingText {
    /* z-index: 1; */
    position: absolute;
    color: white;
    text-align: left;
    font-weight: 450;
    cursor: pointer;
    padding-top: 2%;
    padding-bottom: 2%;
    padding-left: 12%;
    padding-right: 12%;
    top: 12%;
  }
  button {
    position: absolute;
    bottom: 0;
    left: 50%;
  }
  .oval-cursor {
    position: fixed;
    /* left: 10px; */
    z-index: 2;
    width: 1px;
    height: 1px;
    transform: translate(-50%, -50%);
    background-color: white;
    mix-blend-mode: difference;
    border-radius: 50%;
    pointer-events: none;
    transition: width 0.5s, height 0.5s;
  } 
  .oval-cursor.grow.blank {
    width: 80px;
    height: 38px;
  }
  .oval-cursor.grow {
    width: 102px;
    height: 38px;
    border-radius: 50%;
    box-shadow: 30px 0 8px -4px rgba(255, 255, 255, 0.1), -30px 0 8px -4px rgba(255, 255, 255, 0.1);
    background-color: rgba(255, 255, 255, 0.3);
    background-blend-mode: screen;
    pointer-events: none;
    transition: width 0.5s, height 0.5s;
    filter:blur(3px);
  }
  .oval-cursor.grow::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 70%;
    height: 70%;
    background-color: white;
    mix-blend-mode: normal;
    border-radius: 50%;
}
  .blurry-layer {
    position: absolute;
    pointer-events: none;
    color: black;
    text-align: left;
    font-weight: 450;
    padding-top: 2%;
    padding-bottom: 2%;
    padding-left: 12%;
    padding-right: 12%;
    top: 12%;
  }

  * {
    user-select: none; 
    -webkit-user-select: none; 
    -moz-user-select: none; 
    -ms-user-select: none; 
    }
</style>
