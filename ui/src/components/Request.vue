<template>
  <div class="container">

    <div v-if="!error && task">
        <h1 v-if="task.config">Ziming of <a :href="task.config.flags.url" target="_blank">{{ task.config.flags.url }}</a></h1>
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
                <h2>Requesting slot</h2>
                <p>Your request has been recorded and is awaiting a slot on our infrastructure to run.</p>
            </b-alert>
        </div>

        <div v-if="failed">
            <b-alert fade show variant="danger">
                <h2>You request has failed! We are sorry about that.</h2>
                <p>A number of reasons can lead to a ziming failure. Most of the time, it's an inadequate URL… Please triple check it and create a new request. If that doesn't work, <a href="https://github.com/openzim/zimit/issues/new">open a ticket in github</a>.</p>
            </b-alert>
        </div>

        <div v-if="succeeded">
            <b-alert fade show variant="success">
                <h2>Success!</h2>
                <p>The link below will expire and the file will be deleted after a week.</p>
                <a :href="zim_download_url + task.config.warehouse_path + '/' + file.name"><b-button pill variant="grey">Download</b-button></a>
            </b-alert>
        </div>

        <div v-if="ongoing && !is_requested">
            <b-alert fade show variant="info">
                <h2>Your request is being processed</h2>
                <p>One of our servers is currently converting that URL into a nice ZIM file. Depending on the number of pages and resources available, it can be a matter of minutes, hours or even days! Please be patient.</p>
                <p v-if="task.has_email"
                  >You can close this window. You will get an email notification when the task is completed.</p>
            </b-alert>
        </div>
        <div v-if="!Object.isEmpty(flags)">
          <h2>Settings</h2>
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
            return (this.task.container && this.task.container.progress && this.task.container.progress.overall) ? this.task.container.progress.overall : 0; },
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
              return "pending";
            if (this.ended)
              return this.task.status;
            return "in-progress";
          },
          sorted_files() { return Object.values(this.task.files).sortBy('created_timestamp'); },
          file() { return Object.values(this.sorted_files)[0] || {}; },
          zim_download_url() { return Constants.zim_download_url; },
          flags() {
            if (!this.task || !this.task.config.flags)
              return {};
            var parent = this;
            return Object.filter(parent.task.config.flags, function(val, key) {
              if (Constants.hidden_flags.indexOf(key) != -1)
                return false;
              if (key == "limit" && Object.has(parent.task.config.flags, 'limit') && parent.task.config.flags.limit >= Constants.zimit_limit)
                return false;
              return true;
            });
          },
        },
        methods: {
            loadTask() {
                let parent = this;
                parent.toggleLoader("Retrieving task…");
                parent.queryAPI('get', Constants.zimitui_api + '/requests/' + this.task_id)
                  .then(function (response) {
                    if (response.data) {
                      parent.task = response.data;
                      if (parent.ended && parent.interval)
                        clearInterval(parent.interval);
                    } else
                      throw "Didn't receive task";
                  })
                  .catch(function (error) {
                    console.error(error);
                    if (error.response && error.response.status && error.response.status == 404) {
                      parent.alertError("No task found with this ID. It probably has expired.");
                    }
                    else
                      parent.alertError("Unable to retrieve task:\n" + Constants.standardHTTPError(error.response));
                  })
                  .then(function () {
                    parent.toggleLoader(false);
                  });
            },
        },
        mounted() {
          // refresh this periodically
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
