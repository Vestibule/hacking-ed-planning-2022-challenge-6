<script setup lang="ts">
import * as echarts from 'echarts';
import axios from 'axios';
import { ref, onMounted, watch } from 'vue';

enum Charts {
  SCHOOL_ATTENDANCY_BY_YEAR = 'SCHOOL_ATTENDANCY_BY_YEAR',
  SCHOOL_ATTENDANCY_BY_COUNTRY = 'SCHOOL_ATTENDANCY_BY_COUNTRY',
}

const countries = [
  'Argentina',
  'Bolivia',
  'Brasil',
  'Chile',
  'Colombia',
  'Costa Rica',
  'Ecuador',
  'El Salvador',
  'Guatemala',
  'Honduras',
  'México',
  'Nicaragua',
  'Panamá',
  'Paraguay',
  'Perú',
  'República Dominicana',
  'Uruguay',
  'Venezuela',
];

let chart: any = null;
let schoolAttendancyByYearChart: any = null;

const year = ref('0');
const country = ref(null as string | null);
const schoolAttendance = ref([]);
const schoolAttendanceByYear = ref([]);
const chartToDisplay = ref(Charts.SCHOOL_ATTENDANCY_BY_COUNTRY as Charts);
const started = ref(false);

const reloadDataset = async () => {
  const res = await axios.get('http://127.0.0.1:8000/by-gender', {
    params: {
      year: year.value,
    },
  });
  schoolAttendance.value = res.data;
};

const reloadAttendencyByYear = async () => {
  const res = await axios.get('http://127.0.0.1:8000/by-country', {
    params: {
      country: country.value,
    },
  });
  schoolAttendanceByYear.value = res.data;
};

watch(schoolAttendanceByYear, (newSchoolAttendance) => {
  const maleByCountry = newSchoolAttendance.filter(
    (row: any) => row.sex === 'M'
  );
  const femaleByCountry = newSchoolAttendance.filter(
    (row: any) => row.sex === 'F'
  );

  schoolAttendancyByYearChart.setOption({
    title: {
      text: `School attendance ratio evolution in ${country.value} from ${
        maleByCountry[0].year
      } to ${maleByCountry[maleByCountry.length - 1].year}`,
    },
    legend: {
      orient: 'vertical',
      left: 10,
      top: 'center',
    },
    color: ['#91cc75', '#ee6666'],
    tooltip: {},
    xAxis: {
      type: 'time',
    },
    yAxis: {
      name: '% school attendance ratio',
      nameLocation: 'start',
      nameTextStyle: {
        align: 'right',
      },
    },
    series: [
      {
        name: 'Male',
        type: 'line',
        data: maleByCountry.map((row: any) => [
          Date.parse(row.year),
          row.value,
        ]),
        smooth: true,
      },
      {
        name: 'Female',
        type: 'line',
        data: femaleByCountry.map((row: any) => [
          Date.parse(row.year),
          row.value,
        ]),
        smooth: true,
      },
    ],
  });
});

watch(schoolAttendance, (newSchoolAttendance) => {
  const maleByCountry = newSchoolAttendance.filter(
    (row: any) => row.sex === 'M'
  );
  const femaleByCountry = newSchoolAttendance.filter(
    (row: any) => row.sex === 'F'
  );

  chart.setOption({
    legend: {
      orient: 'vertical',
      left: 10,
      top: 'center',
    },
    title: {
      text:
        year.value !== '0'
          ? `School attendance ratio in ${year.value}`
          : 'School attendance ratio',
    },
    color: ['#91cc75', '#ee6666'],
    tooltip: {},
    xAxis: {
      axisLabel: {
        interval: 0,
        rotate: 45,
      },
      data: maleByCountry.map((row: any) => row.country),
      type: 'category',
    },
    yAxis: {
      name: '% school attendance ratio',
      nameLocation: 'start',
      nameTextStyle: {
        align: 'right',
      },
    },
    series: [
      {
        name: 'Male',
        type: 'bar',
        data: maleByCountry.map((row: any) => row.value),
      },
      {
        name: 'Female',
        type: 'bar',
        data: femaleByCountry.map((row: any) => row.value),
      },
    ],
  });
});

watch(year, () => {
  reloadDataset();
  chartToDisplay.value = Charts.SCHOOL_ATTENDANCY_BY_COUNTRY;
});

watch(country, () => {
  reloadAttendencyByYear();
  chartToDisplay.value = Charts.SCHOOL_ATTENDANCY_BY_YEAR;
});

onMounted(async () => {
  const res = await axios.get('http://127.0.0.1:8000/by-gender');
  const schoolAttendance = res.data;

  const maleByCountry = schoolAttendance.filter((row: any) => row.sex === 'M');
  const femaleByCountry = schoolAttendance.filter(
    (row: any) => row.sex === 'F'
  );

  schoolAttendancyByYearChart = echarts.init(
    document.getElementById('chartSchoolAttendancyByYear') as HTMLElement
  );

  chart = echarts.init(document.getElementById('chartElement') as HTMLElement);
  chart.setOption({
    title: {
      text:
        year.value !== '0'
          ? `School attendancy in ${year.value}`
          : 'School attendancy',
    },
    legend: {
      orient: 'vertical',
      left: 10,
      top: 'center',
    },
    color: ['#91cc75', '#ee6666'],
    tooltip: {},
    xAxis: {
      axisLabel: {
        interval: 0,
        rotate: 45,
      },
      data: maleByCountry.map((row: any) => row.country),
      type: 'category',
    },
    yAxis: {
      name: '% school attendance ratio',
      nameLocation: 'start',
      nameTextStyle: {
        align: 'right',
      },
    },
    series: [
      {
        name: 'Male',
        type: 'bar',
        data: maleByCountry.map((row: any) => row.value),
      },
      {
        name: 'Female',
        type: 'bar',
        data: femaleByCountry.map((row: any) => row.value),
      },
    ],
  });
});
</script>

<template>
  <div class="h-screen" :class="started ? 'hidden' : ''">
    <h1 class="mt-4 text-center text-2xl">
      School attendance in Latin America
    </h1>
    <h3 class="w-3/4 mt-8 mx-auto text-lg">
      For this edition of the Hacking Ed Planning, we chose to work on challenge
      6. This challenge consists of displaying data about education in Latin
      American countries.<br />
      We decided to focus on experience. So we chose quality over quantity and
      worked on one metric and one metric only: school attendance.<br />
      We have tried to display it in clear, yet jovial ways.
    </h3>
    <div class="flex justify-center">
      <button @click="started = true" class="mt-4 mx-auto py-2 px-4 border">
        Click here to start
      </button>
    </div>
  </div>
  <div class="flex">
    <div class="h-screen w-1/4 py-2 px-4 flex flex-col space-y-2 shadow">
      <div class="flex flex-col space-y-2">
        <h3 class="text-xl text-center">By year</h3>
        <button
          @click="year = '0'"
          class="w-24 h-8 border rounded"
          :class="
            year === '0' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          All
        </button>
        <button
          @click="year = '2015'"
          class="w-24 h-8 border rounded"
          :class="
            year === '2015' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          2015
        </button>
        <button
          @click="year = '2016'"
          class="w-24 h-8 border rounded"
          :class="
            year === '2016' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          2016
        </button>
        <button
          @click="year = '2017'"
          class="w-24 h-8 border rounded"
          :class="
            year === '2017' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          2017
        </button>
        <button
          @click="year = '2018'"
          class="w-24 h-8 border rounded"
          :class="
            year === '2018' &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_COUNTRY
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          2018
        </button>
      </div>
      <div class="flex flex-col space-y-2 overflow-scroll">
        <h3 class="text-xl text-center">By country</h3>
        <button
          v-for="iteratedCountry in countries"
          :key="iteratedCountry"
          @click="country = iteratedCountry"
          class="w-24 border rounded"
          :class="
            country === iteratedCountry &&
            chartToDisplay === Charts.SCHOOL_ATTENDANCY_BY_YEAR
              ? 'bg-slate-200'
              : 'bg-slate-50'
          "
        >
          {{ iteratedCountry }}
        </button>
      </div>
    </div>
    <canvas
      :class="
        chartToDisplay !== Charts.SCHOOL_ATTENDANCY_BY_COUNTRY ? 'hidden' : ''
      "
      id="chartElement"
      width="1400"
      height="600"
    ></canvas>
    <canvas
      :class="
        chartToDisplay !== Charts.SCHOOL_ATTENDANCY_BY_YEAR ? 'hidden' : ''
      "
      id="chartSchoolAttendancyByYear"
      width="1400"
      height="600"
    ></canvas>
  </div>
</template>
