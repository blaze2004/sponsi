<template>
    <FormContainer title="Update Password">
        <form @submit.prevent="handleSubmit">
            <div class="mb-4">
                <label for="password" class="d-block fw-medium mb-2">New Password</label>
                <input
                    id="password"
                    v-model="formData.password"
                    type="password"
                    required
                    name="password"
                    placeholder="Password"
                    aria-label="Password"
                    class="input"
                />
            </div>
            <div class="mb-4">
                <label for="password2" class="d-block fw-medium mb-2">Confirm Password</label>
                <input
                    id="password2"
                    v-model="formData.password2"
                    type="password"
                    required
                    name="password2"
                    placeholder="Confirm Password"
                    aria-label="Confirm Password"
                    class="input"
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
                password: '',
                password2: '',
            },
        };
    },
    methods: {
        async handleSubmit() {
            const { password, password2 } = this.formData;

            if (!password || !password2) {
                toast.error('All fields are required.');
                return;
            }

            if (password !== password2) {
                toast.error('Passwords do not match.');
                return;
            }

            const formData = new FormData();

            for (const key in this.formData) {
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
