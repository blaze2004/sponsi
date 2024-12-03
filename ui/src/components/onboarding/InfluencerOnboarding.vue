<template>
    <FormContainer title="Influencer Onboarding">
        <form @submit.prevent="handleSubmit">
            <div class="mb-4">
                <label for="niche" class="d-block fw-medium mb-2">What's your Niche?</label>
                <input id="niche" v-model="formData.niche" type="text" required name="niche" placeholder="Niche" aria-label="Niche" class="input" />
            </div>
            <div class="mb-4">
                <label class="d-block fw-medium mb-2">Platform Presence</label>
                <div class="position-relative">
                    <div id="platformPresenceList" class="d-flex w-full overflow-x-scroll gap-2" style="scroll-behavior: smooth">
                        <div v-for="(platform, index) in formData.platforms" :key="index" class="platform-entry p-2 w-full min-w-sm">
                            <div class="d-flex flex-column w-full gap-2">
                                <input
                                    v-model="platform.platform"
                                    type="text"
                                    :name="'platforms-' + index + '-platform'"
                                    placeholder="Platform"
                                    required
                                    class="input"
                                />
                                <input
                                    v-model="platform.username"
                                    type="text"
                                    :name="'platforms-' + index + '-username'"
                                    placeholder="Username"
                                    required
                                    class="input"
                                />
                                <input
                                    v-model="platform.url"
                                    type="url"
                                    :name="'platforms-' + index + '-url'"
                                    placeholder="Profile URL"
                                    required
                                    class="input"
                                />
                                <input
                                    v-model="platform.followers"
                                    type="number"
                                    :name="'platforms-' + index + '-followers'"
                                    placeholder="Followers"
                                    required
                                    class="input"
                                />
                                <button type="button" @click="removePlatform(index)" class="btn btn-danger remove-platform">Remove</button>
                            </div>
                        </div>
                    </div>
                </div>
                <button type="button" @click="addPlatform" class="btn btn-secondary mt-2">Add Platform</button>
            </div>
            <div class="mb-4">
                <label for="category" class="d-block fw-medium mb-2">Category</label>
                <input id="category" v-model="formData.category" type="text" required name="category" aria-label="category" class="input" />
            </div>
            <div class="mb-4">
                <label for="website" class="d-block fw-medium mb-2">Portfolio Website</label>
                <input
                    id="website"
                    v-model="formData.website"
                    type="text"
                    required
                    name="website"
                    placeholder="Website"
                    aria-label="Website"
                    class="input"
                />
            </div>
            <div class="mb-4">
                <label for="about" class="d-block fw-medium mb-2">Bio</label>
                <textarea
                    id="about"
                    v-model="formData.about"
                    required
                    name="about"
                    placeholder="I create content about..."
                    aria-label="About"
                    class="input"
                    style="min-height: 100px"
                />
            </div>
            <div class="mb-4">
                <button type="submit" :disabled="loading" class="w-full btn btn-primary btn-lg"><Spinner v-if="loading" /> &nbsp;Continue</button>
            </div>
        </form>
    </FormContainer>
</template>

<script>
import FormContainer from '@/components/FormContainer.vue';
import submitOnboardingForm from './common';
import { toast } from 'vue-sonner';
import Spinner from '../Spinner.vue';

export default {
    components: { FormContainer, Spinner },
    data() {
        return {
            loading: false,
            formData: {
                niche: '',
                platforms: [
                    {
                        platform: '',
                        username: '',
                        url: '',
                        followers: '',
                    },
                ],
                category: '',
                website: '',
                about: '',
            },
        };
    },
    methods: {
        addPlatform() {
            this.formData.platforms.push({
                platform: '',
                username: '',
                url: '',
                followers: '',
            });
            this.$nextTick(() => {
                const platformList = document.getElementById('platformPresenceList');
                platformList.scrollTo({ left: platformList.scrollWidth, behavior: 'smooth' });
            });
        },
        removePlatform(index) {
            this.formData.platforms.splice(index, 1);
        },
        async handleSubmit() {
            if (!this.formData.niche || !this.formData.category || !this.formData.website || !this.formData.about) {
                toast.error('All fields are required.');
                return;
            }

            const formData = new FormData();

            for (const key in this.formData) {
                if (key === 'platforms') {
                    this.formData.platforms.forEach((platform, index) => {
                        for (const platformKey in platform) {
                            formData.append(`platforms-${index}-${platformKey}`, platform[platformKey]);
                        }
                    });
                    continue;
                }
                formData.append(key, this.formData[key]);
            }

            this.loading = true;
            const res = await submitOnboardingForm(formData);
            this.loading = false;

            if (res) {
                this.$router.push('/dashboard');
            }
        },
    },
};
</script>
