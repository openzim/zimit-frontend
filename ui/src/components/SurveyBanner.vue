<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const SURVEY_URL = 'https://framaforms.org/kiwix-unlimited-zim-creation-platform-1766243846'

const visible = ref(false)
const { t } = useI18n()

onMounted(() => {
  setTimeout(() => {
    visible.value = true
  }, 300) // Wait for fade-in animation
})
</script>

<template>
  <Transition name="fade">
    <div v-if="visible" class="survey-banner">
      <div class="banner-content">
        <div class="banner-text">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm2 14H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"
            />
          </svg>
          <div>
            <h3>{{ t('survey.ctaTitle') }}</h3>
            <p>{{ t('survey.ctaMessage') }}</p>
          </div>
        </div>

        <div class="banner-actions">
          <a :href="SURVEY_URL" target="_blank" rel="noopener noreferrer" class="btn-survey">
            {{ t('survey.buttonTakeSurvey') }}
          </a>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
.survey-banner {
  padding: 16px 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  margin-bottom: 30px;
}

.banner-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 0 auto;
  gap: 24px;
}

.banner-text {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.banner-text svg {
  flex-shrink: 0;
}

.banner-text h3 {
  font-weight: 600;
  font-size: 16px;
  margin: 0 0 4px 0;
}

.banner-text p {
  font-size: 14px;
  margin: 0;
  opacity: 0.8;
}

.banner-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.btn-survey {
  background: #82ca2a;
  color: white;
  padding: 10px 24px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
  transition:
    transform 0.2s,
    box-shadow 0.2s,
    background 0.2s;
  box-shadow: 0 2px 4px rgba(130, 202, 42, 0.3);
}

.btn-survey:hover {
  background: #73b625;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(130, 202, 42, 0.4);
}

.btn-survey:active {
  transform: translateY(0);
}

/* Fade transitions */
.fade-enter-active {
  transition: opacity 0.5s ease-in;
}

.fade-leave-active {
  transition: opacity 0.3s ease-out;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .banner-content {
    flex-direction: column;
    gap: 12px;
  }

  .banner-actions {
    width: 100%;
    flex-direction: column-reverse;
    gap: 8px;
  }

  .btn-survey {
    width: 100%;
    text-align: center;
  }
}
</style>
