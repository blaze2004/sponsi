<template>
    <nav class="navbar navbar-expand-lg fixed-top border-bottom backdrop-blur-xl w-full">
        <div class="container-fluid px-4 mx-auto px-xxl-0 max-w-screen-xl">
            <RouterLink
                to="/"
                class="d-flex align-items-center justify-content-center text-foreground hover:text-muted-foreground dark:hover:text-light"
            >
                <img class="dark:d-none h-8 w-auto" src="@/assets/images/logo.png" alt="logo" />
                <img class="light:d-none dark:d-inline-block h-8 w-auto" src="@/assets/images/logo-dark.png" alt="logo" />
                <h4 class="fs-2 fw-semibold px-2">Sponsi</h4>
            </RouterLink>
            <button class="navbar-toggler" type="button" @click="toggleMenu" :aria-expanded="isMenuOpen" aria-label="Toggle nav drawer">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" :class="{ show: isMenuOpen }" id="navbarMenu">
                <div class="d-flex flex-column flex-lg-row align-items-center justify-content-end w-full gap-2">
                    <template v-if="customNavLinks.length">
                        <RouterLink v-for="(link, index) in filteredNavLinks" :key="index" :to="link.url" class="btn btn-ghost">
                            {{ link.text }}
                        </RouterLink>
                    </template>
                    <template v-if="isAuthenticated">
                        <RouterLink v-if="showDashboardLink" to="/dashboard" class="btn btn-ghost">Dashboard</RouterLink>
                        <button type="submit" class="btn btn-secondary" v-on:click="signOut">Logout</button>
                    </template>
                    <template v-else>
                        <RouterLink to="/signin" class="btn btn-primary">Get Started</RouterLink>
                    </template>
                    <ThemeToggle />
                </div>
            </div>
        </div>
    </nav>
</template>

<script>
import ThemeToggle from '@/components/ThemeChanger.vue';
import { UserRoles } from '@/constants';
import { useUserStore } from '@/stores/user';

export default {
    components: { ThemeToggle },
    data() {
        return {
            isMenuOpen: false,
        };
    },
    computed: {
        userStore() {
            return useUserStore();
        },
        isAuthenticated() {
            return this.userStore.isAuthenticated;
        },
        customNavLinks() {
            const links = [];
            if (this.userStore.onboarded) {
                if (this.userStore.isAuthenticated) {
                    links.push({ text: 'Stats', url: '/stats' });
                }
                if (this.userStore.role === UserRoles.SPONSOR) {
                    links.push({ text: 'Campaigns', url: '/campaigns' }, { text: 'Influencers', url: '/search/influencers' });
                } else if (this.userStore.role === UserRoles.INFLUENCER) {
                    links.push({ text: 'Campaigns', url: '/search/campaigns' });
                }
            }
            return links;
        },
        filteredNavLinks() {
            return this.customNavLinks.filter((link) => link.url !== this.$route.path);
        },
        showDashboardLink() {
            return this.userStore.onboarded && this.$route.path !== '/dashboard';
        },
    },
    methods: {
        toggleMenu() {
            this.isMenuOpen = !this.isMenuOpen;
        },
        async signOut() {
            const success = await this.userStore.signOut();
            if (success) {
                this.$router.push('/');
            }
        },
    },
};
</script>
