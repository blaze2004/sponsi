<template>
    <AdminOnboarding v-if="role === ADMIN" />
    <InfluencerOnboarding v-else-if="role === INFLUENCER" />
    <SponsorOnboarding v-else-if="role === SPONSOR" />
</template>

<script>
import AdminOnboarding from '@/components/onboarding/AdminOnboarding.vue';
import InfluencerOnboarding from '@/components/onboarding/InfluencerOnboarding.vue';
import SponsorOnboarding from '@/components/onboarding/SponsorOnboarding.vue';
import { UserRoles } from '@/constants';
import { useUserStore } from '@/stores/user';

export default {
    components: { AdminOnboarding, InfluencerOnboarding, SponsorOnboarding },
    data() {
        return {
            ...UserRoles,
        };
    },
    computed: {
        role() {
            const userStore = useUserStore();
            return userStore.role;
        },
    },
};
</script>
