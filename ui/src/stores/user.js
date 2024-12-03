import { defineStore } from 'pinia';
import { toast } from 'vue-sonner';

export const useUserStore = defineStore('user', {
    state: () => {
        return {
            isAuthenticated: null,
            role: null /* Admin, Sponsor, Influencer */,
            onboarded: null,
        };
    },
    actions: {
        updateOnboardedStatus(status) {
            this.onboarded = status;
        },
        async checkAuthStatus() {
            try {
                const res = await fetch('/api/auth/status', {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                const response = await res.json();

                if (!res.ok) {
                    this.role = null;
                    this.onboarded = null;
                    this.isAuthenticated = false;
                    return;
                }
                this.role = response.role;
                this.onboarded = response.onboarded;
                this.isAuthenticated = response.isAuthenticated;
            } catch (error) {
                toast.error('Error checking authentication status. Please refresh the page.');
            }
        },

        async signIn({ email, password }) {
            try {
                const res = await fetch('/api/auth/signin', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ email: email, password: password }),
                });

                const data = await res.json();

                if (res.ok) {
                    this.isAuthenticated = true;
                    this.role = data.role;
                    this.onboarded = data.onboarded;
                    toast.success(data.message || 'Signed in successfully.');
                    return true;
                }

                this.isAuthenticated = false;
                this.role = null;
                this.onboarded = null;
                toast.error(data.message || 'Something went wrong.');
            } catch (error) {
                toast.error('Something went wrong.');
            }
            return false;
        },

        async signUp(formData) {
            try {
                const res = await fetch('/api/auth/signup', {
                    method: 'POST',
                    body: formData,
                });

                const data = await res.json();

                if (res.ok) {
                    toast.success(data.message || 'Account created successfully.');
                    return true;
                }
                toast.error(data.message || 'Something went wrong.');
            } catch (error) {
                toast.error('Something went wrong.');
            }
            return false;
        },

        async signOut() {
            try {
                const res = await fetch('/api/auth/signout', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    credentials: 'include',
                });

                if (res.ok) {
                    this.isAuthenticated = false;
                    this.role = null;
                    this.onboarded = null;
                    return true;
                }
            } catch (error) {
                console.error(error);
            }

            return false;
        },
    },
});
