<template>
    <b-card no-body class="mb-1">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-button block v-b-toggle="[id]" variant="neutral">{{ title }}
          <b-icon icon="plus" class="plus" font-scale="1.5"></b-icon>
          <b-icon icon="dash" class="minus" font-scale="1.5"></b-icon></b-button>
      </b-card-header>
      <b-collapse :id="id" visible accordion="faq-accordion" role="tabpanel">
        <b-card-body>
          <b-card-text><slot></slot></b-card-text>
        </b-card-body>
      </b-collapse>
    </b-card>
</template>

<script type="text/javascript">
  export default {
    name: 'FaqEntry',
    props: {
        id: String,
        title: String,
    },
  }
</script>

<style type="text/css" scoped>
  .card-header .btn {
    text-align: left;
  }

  .card-header .plus, .card-header .minus {
    position: absolute;
    top: .5em;
    right: .3rem;
  }
  .card-header .collapsed .minus {
    display: none;
  }
  .card-header .not-collapsed .plus {
    display: none;
  }
</style>
