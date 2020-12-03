<template>
  <div class="container">
    <h1>{{ title }}</h1>

    <div v-if="!error && task">
        <b-progress>
            <b-progress-bar
            :value="task.progress.overall"
            :variant="progress_variant"
            striped
            :animated="ongoing && task.progress.overall > 0 && task.progress.overall < 100">
            {{task.progress.overall.toFixed(0)}}&nbsp;%
            </b-progress-bar>
        </b-progress>

        <div v-if="is_requested">
            <b-alert fade show variant="warning">
                <p>Your request has been recorded and is awaiting a slot on our infrastructure to run.</p>
            </b-alert>
        </div>

        <div v-if="failed">
            <b-alert fade show variant="danger">
                <h2>Your request failed!</h2>
                <p>We're sorry about that but a number of reason can lead to a failure.</p>
                <p>Most of the time, it's an inadequate URL… Please take a quick look at the <em>Error Log</em> bellow for a hint and crete a new request with the fixed options.</p>
                <p>If you can't spot the reason, just contact us.</p>
            </b-alert>
        </div>

        <div v-if="succeeded">
            <b-alert fade show variant="success">
                <h2>Your request succeeded!</h2>
                <p>Please find the link to your ZIM file bellow. Note that this link will expire and the file deleted after a week.</p>
                <a href=""><b-button variant="primary">Download {{ file.name}} ({{ file.size | filesize }})</b-button></a>
            </b-alert>
        </div>

        <div v-if="ongoing">
            <b-alert fade show variant="info">
                <h2>Your request is being processed</h2>
                <p>One of our servers is currently converting that URL into a nice ZIM file. Depending on the number of pages and resources to scrape, it can be a matter of minutes, hours or even days!</p>
                <p>Check the progress bar above with caution as the number of resources to fetch (and thus the total amount of work) evolve over time.</p>
            </b-alert>
        </div>

        <div class="tab-content">
            <table class="table table-responsive-md table-striped table-in-tab">
              <tr><th>ID</th><td><code>{{ task_id }}</code>, <a target="_blank" :href="document_url">document <sup><b-icon icon="arrow-up-right-square" font-scale="1"></b-icon></sup></a></td></tr>
              <tr><th>Status</th><td><code>{{ task.status }}</code></td></tr>
              <tr><th>Worker</th><td>{{ task.worker }}</td></tr>
              <tr v-if="task.files">
                <th>File</th>
                <td>
                  <table class="table table-responsive-md table-striped table-sm">
                    <thead><tr><th>Filename</th><th>Size</th><th>Created After</th><th>Upload Duration</th></tr></thead>
                    <tr v-for="file in sorted_files" :key="file.name">
                      <td><a target="_blank" :href="zimfarm_download_url + task.config.warehouse_path + '/' + file.name">{{ file.name}}</a></td>
                      <td>{{ file.size | filesize }}</td>
                      <td title="file.created_timestamp | format_dt">{{ file | created_after(task) }}</td>
                      <td title="file.uploaded_timestamp | format_dt" v-if="file.status == 'uploaded'">{{ file | upload_duration }}</td>
                      <td v-else>-</td>
                    </tr>
                  </table>
                </td>
              </tr>
              <tr><th>Started On</th><td>{{ started_on|format_dt }}, after <strong>{{ pipe_duration }} in pipe</strong></td></tr>
              <tr><th>Duration</th><td>{{ task_duration }}<span v-if="is_running"> (<strong>Ongoing</strong>)</span></td></tr>
              <tr>
                <th>Events</th>
                <td>
                  <table class="table table-responsive-md table-striped table-sm">
                  <tbody>
                  <tr v-for="event in task.events" v-bind:key="event.code">
                    <td><code>{{ event.code }}</code></td><td>{{ event.timestamp | format_dt }}</td>
                    <td v-if="event.code == 'requested'">{{ task.requested_by }}</td>
                    <td v-else-if="event.code == 'canceled'">{{ task.canceled_by }}</td>
                    <td v-else />
                  </tr>
                  </tbody>
                </table>
                </td>
              </tr>
              <tr v-if="task.config"><th>Offliner</th><td><a target="_blank" :href="'https://hub.docker.com/r/' + task.config.image.name"><code>{{ image_human }}</code></a> (<code>{{ task.config.task_name }}</code>)</td></tr>
              <tr v-if="task.config">
                <th>Resources</th>
                <td>
                  <ResourceBadge kind="cpu" :value="task.config.resources.cpu" />
                  <ResourceBadge kind="memory" :value="task.config.resources.memory" />
                  <ResourceBadge kind="disk" :value="task.config.resources.disk" />
                  <ResourceBadge kind="shm" :value="task.config.resources.shm" v-if="task.config.resources.shm" />
                </td>
              </tr>
              <tr v-if="task.config"><th>Config</th><td><FlagsList :flags="task.config.flags" :shrink="false" /></td></tr>
              <tr v-if="task_container.command"><th>Command </th><td><code class="command">{{ command }}</code></td></tr>
              <tr v-if="task_container.exit_code != null"><th>Exit-code</th><td><code>{{ task_container.exit_code }}</code></td></tr>
              <tr v-if="task_container.stdout"><th>Scraper&nbsp;stdout</th><td><pre class="stdout">{{ task_container.stdout }}</pre></td></tr>
              <tr v-if="task_container.stderr"><th>Scraper&nbsp;stderr</th><td><pre class="stderr">{{ task_container.stderr }}</pre></td></tr>
              <tr v-if="task_container.log"><th>Scrapper&nbsp;Log</th><td><a class="btn btn-secondary btn-sm" target="_blank" :href="'/' + task_container.log">Download log</a></td></tr>
              <tr v-if="task_debug.exception"><th>Exception</th><td><pre>{{ task_debug.exception }}</pre></td></tr>
              <tr v-if="task_debug.traceback"><th>Traceback</th><td><pre>{{ task_debug.traceback }}</pre></td></tr>
              <tr v-if="task_debug.log"><th>Task-worker Log</th><td><pre>{{ task_debug.log }}</pre></td></tr>
            </table>
        </div>
    </div>
    <ErrorMessage v-bind:message="error" v-if="error" />

    </div>
</template>

<script>
    import Constants from '../constants.js'
    import FlagsList from '../components/FlagsList.vue'
    import ResourceBadge from '../components/ResourceBadge.vue'
    import ZimfarmMixins from '../components/mixins.js'

    export default {
        name: 'Request',
        mixins: [ZimfarmMixins],
        components: {FlagsList, ResourceBadge},
        props: {
          task_id: String,  // the zimfarm task ID
        },
        data() {
            return {
                error: null,
                task: null,
            };
        },
        computed: {
          title() { return (this.task) ? this.task.schedule_name : this.task_id; },
          is_requested() { return this.task.status == "requested"; },
          started() { return this.task.status != "requested"; },
          ended() { return this.succeeded === true || this.failed === true; },
          ongoing() { return this.succeeded !== true && this.failed !== true; },
          // succeeded() { return this.task.status == "succeeded" ; },
          succeeded() { return this.task.status == "succeeded" || this.task.status == "scraper_completed" ; }, // awaiting success upload to S3
          failed() { return ["canceled", "cancel_requested", "failed", "scraper_killed"].indexOf(this.task.status) != -1; },
          progress_variant() {
            if (this.succeeded === true)
                return "success";
            if (this.failed === true)
                return "danger";
            return "info";
          },
          document_url() {
            let path = (this.is_requested) ? 'requested-tasks' : 'tasks';
            return Constants.zimfarm_webapi + '/' + path + '/' + this.task_id; },
          sorted_files() { return Object.values(this.task.files).sortBy('created_timestamp'); },
          file() { return Object.values(this.task.files)[0] || {}; },
          short_id() { return Constants.short_id(this.task_id); },
          is_running() { return ["failed", "canceled", "succeeded"].indexOf(this.task.status) == -1; },
          schedule_name() { return this.task ? this.task.schedule_name : null; },
          task_container() { return this.task.container || {}; },
          task_debug() { return this.task.debug || {}; },
          task_duration() {  // duration of a task
            if (!this.task.events)
              return '';

            let first = this.task.timestamp.started;
            if (!first)  // probably in reserved state, hence not yet started
              return "not actually started";

            // if task is running (non-complete status) then it's started-to now
            if (this.is_running) {
              return Constants.format_duration_between(first, Constants.now());
            }

            // if task is not running, it's started to last status
            let last = this.task.updated_at;
            return Constants.format_duration_between(first, last);
          },
          started_on() { return this.task.timestamp.started || this.task.timestamp.reserved; },
          pipe_duration() { return Constants.format_duration_between(this.task.timestamp.requested, this.task.timestamp.started); },
          zimfarm_download_url() { return Constants.zimfarm_download_url; },
          command() { return this.task_container.command.join(" "); },
          image_human() { return Constants.image_human(this.task.config); },
        },
        filters: {
          created_after(value, task) {
            return Constants.format_duration_between(task.timestamp.scraper_started, value.created_timestamp);
          },
          upload_duration(value) {
            return Constants.format_duration_between(value.created_timestamp, value.uploaded_timestamp);
          }
        },
        methods: {
            loadTask() {
                let parent = this;
                parent.toggleLoader("Retrieving task…");
                parent.queryAPI('get', Constants.zimitui_api + '/requests/' + this.task_id)
                  .then(function (response) {
                    console.log(response);
                    if (response.data) {
                      parent.task = response.data;
                    } else
                      throw "Didn't receive task";
                  })
                  .catch(function (error) {
                    if (error.response && error.response.status && error.response.status == 404) {
                        // parent.redirectTo()
                        console.error("NOT FOUND");
                    }
                    parent.alertError("Unable to retrieve schedule:\n" + Constants.standardHTTPError(error.response));
                  })
                  .then(function () {
                    parent.toggleLoader(false);
                  });
            },
        },
        mounted() {
            this.loadTask(false);
        },
    }
</script>

<style type="text/css" scoped>
  .stdout, .stderr {
    max-height: 9rem;
    overflow: scroll;
  }

  table td { padding: .5rem; }
  table th { white-space: nowrap; }
  table caption { caption-side: top; }

  /* Tabs in schedule/task

  first row of table inside a tab should not have a top border
  as the tab has a border right above
  */
  .table-in-tab tr:first-of-type td, .table-in-tab tr:first-of-type th {
      border-top: 0;
  }

  .tab-content {
      background-color: white;
      /*padding: .5rem;*/
      border: 1px solid #dee2e6;
      /*border-top: 0;*/
      border-radius: .25rem;
      overflow-x: scroll;
  }
  .command { word-wrap: anywhere; }

  /* hide pipeline's content while loading/changing */
  table.loading tbody tr td,
  table.loading tbody tr th,
  table.loading tbody tr a,
  table.loading tbody tr code,
  table.loading tbody tr span { color: transparent; }
  table.loading tbody tr span { background-color: transparent; }

  .progress {
    height: 1.5rem;
    margin-bottom: 1rem;
  }

  .progress .progress-bar {
    font-size: 1.5em;
    font-weight: bold;
  }
</style>
