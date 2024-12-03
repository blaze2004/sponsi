<template>
    <FormContainer title="Sponsor Onboarding">
        <form @submit.prevent="handleSubmit">
            <div class="mb-4">
                <label for="company_name" class="d-block fw-medium mb-2">Company Name</label>
                <input
                    id="company_name"
                    v-model="formData.company_name"
                    type="text"
                    required
                    name="company_name"
                    placeholder="Company Name"
                    aria-label="Company Name"
                    class="input"
                />
            </div>
            <div class="mb-4">
                <label for="industry" class="d-block fw-medium mb-2">Industry</label>
                <input
                    id="industry"
                    v-model="formData.industry"
                    type="text"
                    required
                    name="industry"
                    placeholder="Industry"
                    aria-label="Industry"
                    class="input"
                />
            </div>
            <div class="mb-4">
                <label for="website" class="d-block fw-medium mb-2">Website</label>
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
                <label for="monthly_budget" class="d-block fw-medium mb-2">Monthly Budget</label>
                <input
                    id="monthly_budget"
                    v-model="formData.monthly_budget"
                    type="number"
                    name="monthly_budget"
                    placeholder="200000"
                    aria-label="monthly_budget"
                    class="input"
                />
            </div>
            <div class="mb-4">
                <label for="about" class="d-block fw-medium mb-2">About the Company</label>
                <textarea
                    id="about"
                    v-model="formData.about"
                    required
                    name="about"
                    placeholder="We are..."
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
    components: { FormContainer , Spinner},
    data() {
        return {
            loading: false,
            formData: {
                company_name: '',
                industry: '',
                website: '',
                about: '',
                monthly_budget: '',
            },
        };
    },
    methods: {
        async handleSubmit() {
            const { company_name, industry, website } = this.formData;

            if (!company_name || !industry || !website) {
                toast.error('All fields are required.');
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
