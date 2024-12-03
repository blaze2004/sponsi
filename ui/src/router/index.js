import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import { useUserStore } from '@/stores/user';

const routeMeta = ({ requiresAuth = false, requiresRole = null, requiresOnboarding = false, roles = [] } = {}) => {
    return {
        requiresAuth,
        requiresRole,
        requiresOnboarding,
        roles,
    };
};

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
            meta: routeMeta(),
        },
        {
            path: '/signin',
            name: 'signin',
            component: () => import('../views/auth/SignInView.vue'),
            meta: routeMeta(),
        },
        {
            path: '/signup',
            name: 'signup',
            component: () => import('../views/auth/SignUpView.vue'),
            meta: routeMeta(),
        },
        {
            path: '/onboarding',
            name: 'onboarding',
            component: () => import('../views/auth/OnboardingView.vue'),
            meta: routeMeta({ requiresAuth: true }),
        },
        {
            path: '/dashboard',
            name: 'dashboard',
            component: () => import('../views/DashboardView.vue'),
            meta: routeMeta({ requiresAuth: true, requiresOnboarding: true }),
        },
    ],
});

router.beforeEach(async (to, _, next) => {
    const authStore = useUserStore();

    if (authStore.isAuthenticated === null) {
        await authStore.checkAuthStatus();
    }

    if (['signin', 'signup'].includes(to.name) && authStore.isAuthenticated) {
        next({ name: 'dashboard' });
    } else if (to.name == 'onboarding' && authStore.onboarded) {
        next({ name: 'dashboard' });
    } else if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next({ name: 'signin' });
    } else if (to.meta.requiresOnboarding && !authStore.onboarded) {
        next({ name: 'onboarding' });
    } else if (to.meta.requiresRole && !to.meta.roles.includes(authStore.role)) {
        next({ name: 'home' });
    } else {
        next();
    }
});

export default router;
