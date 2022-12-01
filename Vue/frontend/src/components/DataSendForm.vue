<template>
  <div>
    <div>시작일 <input type="date" v-model="startDate" /></div>
    <div>종료일 <input type="date" v-model="endDate" /></div>
    <select v-model="timeUnit">
      <option value="date">일간</option>
      <option value="week">주간</option>
      <option value="month">월간</option>
    </select>
    <div>
      그룹명: <input type="text" v-model="userInputGroupName" />
      <button v-on:click="tempGroupAdd">추가</button>
      {{ tempGroupName }}
    </div>
    <div>
      키워드: <input type="text" v-model="userInputKeyword" />
      <button v-on:click="tempKeywordAdd">추가</button>
      {{ tempKeywords }}
    </div>
    <div>
      <button v-on:click="makeGroup">그룹 확정</button>
    </div>
    <div>
      <div>사용자 입력 그룹별 키워드</div>
      <div v-if="keywordGroups.length">
        <div v-for="(keywordGroup, index) in keywordGroups" v-bind:key="index">
          <div>그룹 이름: {{ keywordGroup.groupName }}</div>
          <div>그룹 키워드: {{ keywordGroup.keywords }}</div>
        </div>
      </div>
    </div>
    <div>
      <input type="submit" v-on:click="sendResultToApi" />
    </div>
  </div>
</template>

<script>
import { dataLab } from "../utils/axios";
export default {
  data() {
    return {
      startDate: "",
      endDate: "",
      timeUnit: "month",
      keywordGroups: [],
      userInputGroupName: "",
      userInputKeyword: "",
      tempGroupName: "",
      tempKeywords: [],
      toApiData: {},
    };
  },
  methods: {
    tempGroupAdd() {
      this.tempGroupName = this.userInputGroupName;
    },
    tempKeywordAdd() {
      this.tempKeywords.push(this.userInputKeyword);
      this.userInputKeyword = "";
    },
    makeGroup() {
      this.keywordGroups.push({
        groupName: this.tempGroupName,
        keywords: this.tempKeywords,
      });
      this.tempGroupName = "";
      this.tempKeywords = [];
      this.userInputGroupName = "";
    },
    async sendResultToApi() {
      this.toApiData = {
        startDate: this.startDate,
        endDate: this.endDate,
        timeUnit: this.timeUnit,
        keywordGroups: this.keywordGroups,
      };
      await dataLab.post(this.toApiData);
      console.log(this.toApiData);
      location.reload();
    },
  },
};
</script>

<style scoped></style>