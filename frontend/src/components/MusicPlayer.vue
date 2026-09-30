<template>
	<div class="music-player hidden lg:flex lg:flex-col fixed left-0 bottom-0 w-52 xl:w-56 border-t border-white/10 bg-white/5 backdrop-blur px-3 pt-4 pb-4 z-10">
		<!-- 加载状态 -->
		<div v-if="loadingSongs" class="flex items-center justify-center py-8 text-white/60 text-sm">
			加载歌曲中...
		</div>
		<!-- 错误提示 -->
		<div v-else-if="songsError" class="flex items-center justify-center py-8 px-2 text-red-400 text-xs text-center">
			{{ songsError }}
		</div>
		<!-- 播放器内容 -->
		<template v-else-if="playlist.length > 0">
		<!-- 唱片容器 -->
		<div class="flex flex-col items-center mb-4">
			<!-- 旋转的唱片 -->
			<div class="relative mb-3">
				<div 
					class="w-32 h-32 rounded-full bg-gradient-to-br from-gray-800 to-gray-900 shadow-2xl relative overflow-hidden record-disc"
					:class="{ 'playing': isPlaying }"
				>
					<!-- 唱片背景纹理 -->
					<div class="absolute inset-0 flex items-center justify-center">
						<div class="w-full h-full rounded-full border-4 border-white/5"></div>
					</div>
					<!-- 同心圆纹理 -->
					<div class="absolute inset-2 rounded-full border-2 border-white/10"></div>
					<div class="absolute inset-4 rounded-full border border-white/5"></div>
					<!-- 中心圆点 -->
					<div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-black z-10 border-2 border-white/20"></div>
					<!-- 唱片封面图片 -->
					<div class="absolute inset-2 rounded-full overflow-hidden">
						<img 
							v-if="currentSong.cover"
							:src="currentSong.cover"
							:alt="currentSong.name"
							class="w-full h-full object-cover"
						/>
						<div 
							v-else
							class="w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-600 to-purple-600"
						>
							<svg class="w-12 h-12 text-white/80" fill="currentColor" viewBox="0 0 20 20">
								<path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z" />
							</svg>
						</div>
					</div>
				</div>
			</div>
			
			<!-- 歌曲信息 -->
			<div class="text-center w-full px-2">
				<div class="text-sm font-medium text-white truncate mb-1">
					{{ currentSong.name }}
				</div>
				<div class="text-xs text-white/60 truncate mb-3">
					{{ currentSong.artist }}
				</div>
			</div>
		</div>

		<!-- 播放控制 -->
		<div class="flex flex-col gap-2 px-2">
			<!-- 进度条 -->
			<div class="relative">
				<div class="h-1 bg-white/10 rounded-full overflow-hidden">
					<div 
						class="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300"
						:style="{ width: progressPercent + '%' }"
					></div>
				</div>
				<input
					type="range"
					min="0"
					:max="duration"
					:value="currentTime"
					@input="handleSeek"
					class="absolute inset-0 w-full h-1 opacity-0 cursor-pointer"
				/>
			</div>

			<!-- 时间显示 -->
			<div class="flex items-center justify-between text-xs text-white/50 px-1">
				<span>{{ formatTime(currentTime) }}</span>
				<span>{{ formatTime(duration) }}</span>
			</div>

			<!-- 控制按钮 -->
			<div class="flex items-center justify-center gap-3">
				<!-- 上一首 -->
				<button
					@click="prevSong"
					class="p-2 rounded-full hover:bg-white/10 transition-colors text-white/70 hover:text-white"
					title="上一首"
				>
					<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
						<path d="M8.445 14.832A1 1 0 0010 14v-2.798l5.445 3.63A1 1 0 0017 14V6a1 1 0 00-1.555-.832L10 8.798V6a1 1 0 00-1.555-.832l-6 4a1 1 0 000 1.664l6 4z" />
					</svg>
				</button>
				
				<!-- 播放/暂停 -->
				<button
					@click="togglePlay"
					class="p-3 rounded-full bg-white/10 hover:bg-white/20 transition-colors text-white"
					title="播放/暂停"
				>
					<svg v-if="!isPlaying" class="w-5 h-5 ml-0.5" fill="currentColor" viewBox="0 0 20 20">
						<path d="M6.3 2.841A1.5 1.5 0 004 4.11V15.89a1.5 1.5 0 002.3 1.269l9.344-5.89a1.5 1.5 0 000-2.538L6.3 2.84z" />
					</svg>
					<svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
						<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
					</svg>
				</button>
				
				<!-- 下一首 -->
				<button
					@click="nextSong"
					class="p-2 rounded-full hover:bg-white/10 transition-colors text-white/70 hover:text-white"
					title="下一首"
				>
					<svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
						<path d="M4.555 5.168A1 1 0 003 6v8a1 1 0 001.555.832L10 11.202V14a1 1 0 001.555.832l6-4a1 1 0 000-1.664l-6-4A1 1 0 0011 6v2.798l-5.445-3.63z" />
					</svg>
				</button>
			</div>

			<!-- 音量控制 -->
			<div class="flex items-center gap-2 px-1 mt-2">
				<!-- 静音按钮 -->
				<button
					@click="toggleMute"
					class="p-1.5 rounded-full hover:bg-white/10 transition-colors text-white/70 hover:text-white flex-shrink-0"
					:title="isMuted ? '取消静音' : '静音'"
				>
					<!-- 静音图标 -->
					<svg v-if="isMuted || volume === 0" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
						<path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM12.293 7.293a1 1 0 011.414 0L15 8.586l1.293-1.293a1 1 0 111.414 1.414L16.414 10l1.293 1.293a1 1 0 01-1.414 1.414L15 11.414l-1.293 1.293a1 1 0 01-1.414-1.414L13.586 10l-1.293-1.293a1 1 0 010-1.414z" clip-rule="evenodd" />
					</svg>
					<!-- 低音量图标（一条波浪线） -->
					<svg v-else-if="volume < 0.5" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
						<path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM12 9a1 1 0 011.414 0A3 3 0 0115 12a1 1 0 11-2 0 1 1 0 00-1.707-.707A1 1 0 0112 9z" clip-rule="evenodd" />
					</svg>
					<!-- 高音量图标（多条波浪线） -->
					<svg v-else class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
						<path fill-rule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 01-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.984 5.984 0 01-1.757 4.243 1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.983 3.983 0 00-1.172-2.828 1 1 0 010-1.415z" clip-rule="evenodd" />
					</svg>
				</button>
				
				<!-- 音量滑块 -->
				<div class="flex-1 relative">
					<div class="h-1 bg-white/10 rounded-full overflow-hidden">
						<div 
							class="h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-300"
							:style="{ width: (isMuted ? 0 : volume * 100) + '%' }"
						></div>
					</div>
					<input
						type="range"
						min="0"
						max="1"
						step="0.01"
						:value="isMuted ? 0 : volume"
						@input="handleVolumeChange"
						class="absolute inset-0 w-full h-1 opacity-0 cursor-pointer"
					/>
				</div>
				
				<!-- 音量百分比显示（可选） -->
				<span class="text-xs text-white/50 w-8 text-right">
					{{ Math.round((isMuted ? 0 : volume) * 100) }}%
				</span>
			</div>
		</div>

		<!-- 音频元素 -->
		<audio
			ref="audioRef"
			:src="currentSong.url"
			@loadedmetadata="onLoadedMetadata"
			@timeupdate="onTimeUpdate"
			@ended="onEnded"
			preload="metadata"
		></audio>
		</template>
		<!-- 空状态 -->
		<div v-else class="flex items-center justify-center py-8 text-white/60 text-sm text-center px-2">
			暂无歌曲
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, onActivated, onDeactivated, watch } from 'vue';

import { songs } from '@/lib/content';

// 从 localStorage 恢复状态的辅助函数
const loadState = () => {
	try {
		const saved = localStorage.getItem('musicPlayerState');
		if (saved) {
			const state = JSON.parse(saved);
			return {
				currentIndex: state.currentIndex ?? 0,
				volume: state.volume ?? 0.7,
				isMuted: state.isMuted ?? false,
				previousVolume: state.previousVolume ?? 0.7,
				currentTime: state.currentTime ?? 0,
				isPlaying: state.isPlaying ?? false // 恢复播放状态
			};
		}
	} catch (e) {
		console.error('恢复播放器状态失败:', e);
	}
	return {
		currentIndex: 0,
		volume: 0.7,
		isMuted: false,
		previousVolume: 0.7,
		currentTime: 0,
		isPlaying: false
	};
};

// 保存状态到 localStorage
const saveState = () => {
	try {
		const state = {
			currentIndex: currentIndex.value,
			volume: volume.value,
			isMuted: isMuted.value,
			previousVolume: previousVolume.value,
			currentTime: audioRef.value?.currentTime ?? currentTime.value,
			isPlaying: isPlaying.value
		};
		localStorage.setItem('musicPlayerState', JSON.stringify(state));
	} catch (e) {
		console.error('保存播放器状态失败:', e);
	}
};

// 播放列表（从后端API获取）
const playlist = ref(songs);
const loadingSongs = ref(false);
const songsError = ref('');

// 从后端加载歌曲列表
const loadSongs = async () => {
	loadingSongs.value = false;
	songsError.value = '';
	const savedState = loadState();
	if (savedState.currentIndex >= playlist.value.length) currentIndex.value = 0;
};

// 从 localStorage 恢复状态
const initialState = loadState();

const audioRef = ref(null);
const isPlaying = ref(initialState.isPlaying); // 从 localStorage 恢复播放状态
const currentIndex = ref(initialState.currentIndex);
const currentTime = ref(initialState.currentTime);
const duration = ref(0);
const volume = ref(initialState.volume);
const isMuted = ref(initialState.isMuted);
const previousVolume = ref(initialState.previousVolume);
let lastSaveTime = 0; // 上次保存时间戳

const currentSong = computed(() => playlist.value[currentIndex.value] || {});

const progressPercent = computed(() => {
	if (duration.value === 0) return 0;
	return (currentTime.value / duration.value) * 100;
});

// 播放/暂停
const togglePlay = async () => {
	if (!audioRef.value) return;
	
	if (isPlaying.value) {
		audioRef.value.pause();
		isPlaying.value = false;
	} else {
		try {
			await audioRef.value.play();
			isPlaying.value = true;
		} catch (error) {
			console.error('播放失败:', error);
			isPlaying.value = false;
		}
	}
	saveState();
};

// 上一首
const prevSong = async () => {
	const wasPlaying = isPlaying.value;
	if (currentIndex.value > 0) {
		currentIndex.value--;
	} else {
		currentIndex.value = playlist.value.length - 1;
	}
	
	if (audioRef.value) {
		isPlaying.value = false;
		audioRef.value.load();
		if (wasPlaying) {
			audioRef.value.addEventListener('loadeddata', () => {
				togglePlay();
			}, { once: true });
		}
	}
	saveState();
};

// 下一首
const nextSong = async () => {
	const wasPlaying = isPlaying.value;
	if (currentIndex.value < playlist.value.length - 1) {
		currentIndex.value++;
	} else {
		currentIndex.value = 0;
	}
	
	if (audioRef.value) {
		isPlaying.value = false;
		audioRef.value.load();
		if (wasPlaying) {
			audioRef.value.addEventListener('loadeddata', () => {
				togglePlay();
			}, { once: true });
		}
	}
	saveState();
};

// 进度条拖拽
const handleSeek = (e) => {
	if (!audioRef.value) return;
	const seekTime = (e.target.value / duration.value) * duration.value;
	audioRef.value.currentTime = seekTime;
	currentTime.value = seekTime;
};

// 音量控制
const handleVolumeChange = (e) => {
	if (!audioRef.value) return;
	const newVolume = parseFloat(e.target.value);
	volume.value = newVolume;
	audioRef.value.volume = newVolume;
	
	// 如果音量大于0，取消静音
	if (newVolume > 0 && isMuted.value) {
		isMuted.value = false;
	}
	// 如果音量设为0，自动静音
	if (newVolume === 0) {
		isMuted.value = true;
	}
	saveState();
};

// 静音/取消静音
const toggleMute = () => {
	if (!audioRef.value) return;
	
	if (isMuted.value) {
		// 取消静音，恢复之前的音量
		isMuted.value = false;
		volume.value = previousVolume.value > 0 ? previousVolume.value : 0.7;
		audioRef.value.volume = volume.value;
	} else {
		// 静音，保存当前音量
		previousVolume.value = volume.value;
		isMuted.value = true;
		volume.value = 0;
		audioRef.value.volume = 0;
	}
	saveState();
};

// 格式化时间
const formatTime = (seconds) => {
	if (isNaN(seconds)) return '0:00';
	const mins = Math.floor(seconds / 60);
	const secs = Math.floor(seconds % 60);
	return `${mins}:${secs.toString().padStart(2, '0')}`;
};

// 恢复播放进度的函数
const restorePlaybackPosition = () => {
	if (!audioRef.value) return;
	
	const savedTime = currentTime.value;
	// 如果没有保存的进度，不恢复
	if (savedTime <= 0) return;
	
	// 如果音频已经加载了元数据，直接恢复
	if (audioRef.value.readyState >= 1 && audioRef.value.duration) {
		if (savedTime < audioRef.value.duration) {
			audioRef.value.currentTime = savedTime;
		}
	} else {
		// 否则等待元数据加载完成
		const handler = () => {
			if (audioRef.value && audioRef.value.duration) {
				const timeToRestore = currentTime.value;
				if (timeToRestore > 0 && timeToRestore < audioRef.value.duration) {
					audioRef.value.currentTime = timeToRestore;
				}
			}
		};
		audioRef.value.addEventListener('loadedmetadata', handler, { once: true });
	}
};

// 音频事件处理
const onLoadedMetadata = () => {
	if (audioRef.value) {
		duration.value = audioRef.value.duration;
		// 元数据加载完成后恢复播放进度
		// 注意：只有在不是切换歌曲的情况下才恢复（切换歌曲时 currentTime 会被重置为 0）
		if (!isChangingSong) {
			const savedTime = currentTime.value;
			if (savedTime > 0 && savedTime < duration.value) {
				// 使用 setTimeout 确保在音频元素完全准备好后再设置
				setTimeout(() => {
					if (audioRef.value && savedTime < audioRef.value.duration) {
						audioRef.value.currentTime = savedTime;
					}
				}, 50);
			}
		}
	}
};

const onTimeUpdate = () => {
	if (audioRef.value) {
		currentTime.value = audioRef.value.currentTime;
		// 定期保存播放进度（每5秒保存一次，避免频繁写入）
		const now = Date.now();
		if (now - lastSaveTime > 5000) {
			saveState();
			lastSaveTime = now;
		}
	}
};

// 记录是否应该自动播放下一首（用于 onEnded 事件）
let shouldAutoPlayNext = false;

const onEnded = () => {
	isPlaying.value = false;
	// 标记应该自动播放下一首
	shouldAutoPlayNext = true;
	// 自动播放下一首
	if (currentIndex.value < playlist.value.length - 1) {
		currentIndex.value++;
	} else {
		currentIndex.value = 0;
	}
	// watch(currentIndex) 会自动调用 load()，我们在那里处理自动播放
};

// 记录是否正在切换歌曲（用于区分是切换歌曲还是页面切换）
let isChangingSong = false;

// 监听歌曲变化
watch(currentIndex, (newIndex, oldIndex) => {
	if (audioRef.value && oldIndex !== undefined && oldIndex !== newIndex) {
		// 只有在真正切换歌曲时才重置进度
		isChangingSong = true;
		currentTime.value = 0;
		
		// 加载新歌曲
		audioRef.value.load();
		
		// 如果应该自动播放（比如歌曲播放完毕自动切换），则自动播放
		if (shouldAutoPlayNext) {
			audioRef.value.addEventListener('loadeddata', async () => {
				try {
					await audioRef.value.play();
					isPlaying.value = true;
				} catch (error) {
					console.error('自动播放下一首失败:', error);
					isPlaying.value = false;
				}
				shouldAutoPlayNext = false;
			}, { once: true });
		}
		
		// 切换歌曲后保持音量设置
		setTimeout(() => {
			if (audioRef.value) {
				audioRef.value.volume = isMuted.value ? 0 : volume.value;
			}
			isChangingSong = false;
		}, 100);
	}
	saveState();
});

// 监听音量变化，同步到音频元素
watch(volume, (newVolume) => {
	if (audioRef.value && !isMuted.value) {
		audioRef.value.volume = newVolume;
	}
});

// 监听静音状态变化
watch(isMuted, (muted) => {
	if (audioRef.value) {
		audioRef.value.volume = muted ? 0 : volume.value;
	}
});

// 初始化音频元素的函数
const initializeAudio = async () => {
	if (audioRef.value) {
		audioRef.value.volume = isMuted.value ? 0 : volume.value;
		// 恢复播放进度（如果之前有保存）
		restorePlaybackPosition();
		
		// 同步播放状态：如果 isPlaying 为 true 但 audio 实际未播放，则同步状态
		// 或者尝试恢复播放（但浏览器可能阻止自动播放）
		if (isPlaying.value) {
			// 等待音频加载完成后再尝试播放
			const tryRestorePlayback = async () => {
				if (audioRef.value && audioRef.value.readyState >= 2) {
					try {
						await audioRef.value.play();
						// 播放成功，状态已同步
						isPlaying.value = true;
					} catch (error) {
						// 播放失败（可能是浏览器阻止自动播放），同步状态为暂停
						console.log('恢复播放失败（可能是浏览器阻止自动播放）:', error);
						isPlaying.value = false;
						saveState();
					}
				} else {
					// 如果还没加载完成，等待加载完成
					audioRef.value.addEventListener('canplay', tryRestorePlayback, { once: true });
				}
			};
			
			// 延迟一下，确保音频元素已经准备好
			setTimeout(tryRestorePlayback, 100);
		} else {
			// 如果状态是暂停，确保 audio 也是暂停状态
			if (!audioRef.value.paused) {
				audioRef.value.pause();
			}
		}
	}
};

onMounted(() => {
	// 先加载歌曲列表
	loadSongs().then(() => {
		// 歌曲加载完成后再初始化音频
		initializeAudio();
	});
});

// 当组件被 keep-alive 激活时（现在在 Root.vue 中，不会因为路由切换而停用）
onActivated(() => {
	initializeAudio();
});

// 当组件被 keep-alive 停用时（现在在 Root.vue 中，通常不会触发）
onDeactivated(() => {
	// 保存状态
	saveState();
});

// 当组件真正被卸载时（比如关闭标签页）
onUnmounted(() => {
	// 组件卸载前保存状态
	saveState();
	if (audioRef.value) {
		// 只有在真正卸载时才暂停（比如关闭页面）
		audioRef.value.pause();
		audioRef.value = null;
	}
});
</script>

<style scoped>
@keyframes rotate {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}

.record-disc {
	will-change: transform;
}

.record-disc.playing {
	animation: rotate 8s linear infinite;
}

.record-disc:not(.playing) {
	animation: none;
}

/* 自定义进度条样式 */
input[type="range"] {
	-webkit-appearance: none;
	appearance: none;
	background: transparent;
}

input[type="range"]::-webkit-slider-thumb {
	-webkit-appearance: none;
	appearance: none;
	width: 12px;
	height: 12px;
	border-radius: 50%;
	background: white;
	cursor: pointer;
	opacity: 0;
	transition: opacity 0.2s;
}

input[type="range"]:hover::-webkit-slider-thumb {
	opacity: 1;
}

input[type="range"]::-moz-range-thumb {
	width: 12px;
	height: 12px;
	border-radius: 50%;
	background: white;
	cursor: pointer;
	border: none;
	opacity: 0;
	transition: opacity 0.2s;
}

input[type="range"]:hover::-moz-range-thumb {
	opacity: 1;
}
</style>
