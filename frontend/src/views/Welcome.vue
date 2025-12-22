<template>
  <div class="h-screen w-full overflow-hidden relative">
    <SiteHeader />
    <Vortex
      background-color="black"
      :range-y="800"
      :particle-count="500"
      :base-hue="120"
      class="flex size-full flex-col items-center justify-center px-2 pb-2 pt-8 md:px-10"
    >
      <ClientOnly>
        <BlurReveal
          :delay="0.2"
          :duration="0.75"
          class="flex max-w-2xl flex-col items-center gap-4 p-6 text-white"
        >
          <img
            src="/logo.png"
            alt="Area-Ivy logo"
            class="h-16 w-auto object-contain sm:h-20"
          />
          <h2 class="text-center text-3xl font-bold tracking-tighter text-white sm:text-5xl md:text-6xl whitespace-nowrap">
            Hi there, welcome to my blog.
          </h2>
          <TextGenerateEffect
            class="text-center text-base tracking-tight text-white/90 sm:text-xl md:text-2xl"
            :duration="1"
            :delay="200"
            words="Thoughts on building, experimenting, and documenting the creative process behind this blog."
          />
          <div class="mt-6 flex items-center justify-center">
            <RainbowButton :is="RouterLink" to="/home">
              Tap to Start Exploring
            </RainbowButton>
          </div>
        </BlurReveal>
      </ClientOnly>
    </Vortex>
  </div>
</template>

<script setup>
import Vortex from '../components/Vortex.vue';
import SiteHeader from '@/components/SiteHeader.vue';
import BlurReveal from '@/components/BlurReveal.vue';
import ClientOnly from '@/components/ClientOnly.vue';
import TextGenerateEffect from '@/components/TextGenerateEffect.vue';
import RainbowButton from '@/components/RainbowButton.vue';
import { RouterLink } from 'vue-router';
</script>