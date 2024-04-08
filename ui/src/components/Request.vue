<template>
  <div class="container">

    <div v-if="!error && task">
        <h1 v-if="task && task.config">{{ $t('request.zimingOf') }}<a :href="task.config.flags.url" target="_blank">{{ task.config.flags.url }}</a></h1>
        <b-progress>
            <b-progress-bar
            :value="progression"
            :variant="progress_variant"
            striped
            :animated="ongoing"
            :class="visibility_fix">
            {{progression.toFixed(0)}}&nbsp;% ({{ simple_status }})
            </b-progress-bar>
        </b-progress>

        <div v-if="is_requested">
            <b-alert fade show variant="warning">
                <h2>{{$t('request.requestingSlot')}}</h2>
                <p>{{$t('request.requestRecorded')}}</p>
            </b-alert>
        </div>

        <div v-if="failed">
            <b-alert fade show variant="danger">
                <h2>{{$t('request.requestFailed')}}</h2>
                <p>{{$t('request.failureReasons')}} <a href="https://github.com/openzim/zimit/issues/new">{{$t('request.openTicket')}}</a>.</p>
            </b-alert>
        </div>

        <div v-if="succeeded">
            <b-alert fade show variant="success">
                <h2>{{$t('request.success')}}</h2>
                <p>{{$t('request.linkExpires')}}</p>
                <p><a :href="zim_download_url + task.config.warehouse_path + '/' + file.name"><b-button pill variant="grey">{{$t('request.download')}}</b-button></a></p>
                <p v-if="limit_hit">{{$t('request.limitHit')}}</p>
            </b-alert>
        </div>

        <div v-if="ongoing && !is_requested">
            <b-alert fade show variant="info">
                <h2>{{$t('request.beingProcessed')}}</h2>
                <p>{{$t('request.serverConverting')}}</p>
                <p v-if="task.has_email">{{$t('request.emailNotification')}}</p>
            </b-alert>
        </div>
        <div v-if="!Object.isEmpty(flags)">
          <h2>{{$t('request.title')}}</h2>
          <FlagsList :flags="flags" :shrink="false" />
        </div>
    </div>
    <ErrorMessage v-bind:message="error" v-if="error" />

    </div>
</template>

<script>
import Constants from '../constants.js'
import FlagsList from '../components/FlagsList.vue'
import ZimfarmMixins from '../components/mixins.js'

export default {
    name: 'Request',
    mixins: [ZimfarmMixins],
    components: {FlagsList},
    props: {
      task_id: String,  // the zimfarm task ID
    },
    data() {
        return {
            error: null,
            task: null,
            interval: null,
        };
    },
    computed: {
      is_requested() { return this.task.status == "requested"; },
      ended() { return this.succeeded === true || this.failed === true; },
      ongoing() { return this.succeeded !== true && this.failed !== true; },
      succeeded() { return this.task.status == "succeeded"; },
      failed() { return ["canceled", "cancel_requested", "failed", "scraper_killed"].indexOf(this.task.status) != -1; },
      progression() {
        if (this.ended)
          return 100;
        return (this.task.container && this.task.container.progress && this.task.container.progress.overall) ? this.task.container.progress.overall : 0; 
      },
      visibility_fix() {
        if (this.progression < 15)
          return "visible-text";
        return "";
      },
      progress_variant() {
        if (this.succeeded === true)
            return "success";
        if (this.failed === true)
            return "danger";
        return "info";
      },
      simple_status() {
        if (this.is_requested)
          return this.$t('request.pending');
        if (this.ended)
          return this.task.status;
        return this.$t('request.inProgress');
      },
      sorted_files() { return Object.values(this.task.files).sort((a, b) => a.created_timestamp - b.created_timestamp); },
      file() { return this.sorted_files[0] || {}; },
      zim_download_url() { return Constants.zim_download_url; },
      flags() {
        if (!this.task || !this.task.config || !this.task.config.flags)
          return {};
        return Object.entries(this.task.config.flags)
          .filter(([key, val]) => !Constants.hidden_flags.includes(key) && 
                  !(key === "size_limit" && val >= Constants.zimit_size_limit) && 
                  !(key === "time_limit" && val >= Constants.zimit_time_limit))
          .reduce((obj, [key, val]) => ({ ...obj, [key]: val }), {});
      },
      human_size_limit() {
          const sizeInGiB = parseInt(Constants.zimit_size_limit / 1073741824);
          return this.$t('request.humanSizeLimit', { size: sizeInGiB });
      },
      human_time_limit() {
          const timeInHours = parseInt(Constants.zimit_time_limit / 3600);
          const unitKey = `units.timeLimit.${timeInHours === 1 ? 'hour' : 'hours'}`;
          return this.$t('request.humanTimeLimit', {
            hours: timeInHours, 
            unit: this.$t(unitKey)
        });
      },
      limit_hit() { 
          return this.task.container && this.task.container.progress && this.task.container.progress.limit && this.task.container.progress.limit.hit;
      },
    },
    methods: {
        loadTask() {
            this.toggleLoader(this.$t('request.loadingTask'));
            this.queryAPI('get', `${Constants.zimitui_api}/requests/${this.task_id}`)
              .then(response => {
                if (response.data) {
                  this.task = response.data;
                  if (this.ended && this.interval) clearInterval(this.interval);
                } else {
                  throw new Error(this.$t('request.noDataReceived'));
                }
              })
              .catch(error => {
                console.error(error);
                if (error.response && error.response.status === 404) {
                  this.alertError(this.$t('request.taskNotFound'));
                } else {
                  this.alertError(this.$t('request.taskRetrieveError', { error: Constants.standardHTTPError(error.response) }));
                }
              })
              .then(() => {
                this.toggleLoader(false);
              });
        },
    },
    mounted() {
      this.loadTask(false);
      this.interval = setInterval(this.loadTask, Constants.zimit_refresh_after * 1000, false);
    },
}
</script>

<style type="text/css" scoped>
  table td { padding: .5rem; }
  table th { white-space: nowrap; }
  table caption { caption-side: top; }

  .progress {
    height: 1.5rem;
    margin-bottom: 1rem;
  }

  .progress .progress-bar {
    font-size: 1.5em;
    font-weight: bold;
  }
  .visible-text {
    overflow: visible;
    color: rgb(102, 102, 102);
  }

  .alert {
    margin-bottom: 2em;
  }

  code {
    color: rgb(30, 30, 30);
  }
</style>
