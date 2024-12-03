import { useUserStore } from '@/stores/user';
import { toast } from 'vue-sonner';

const submitOnboardingForm = async (formData) => {
    try {
        const res = await fetch('/api/auth/onboarding', {
            method: 'POST',
            body: formData,
        });

        const data = await res.json();

        if (res.ok) {
            const userStore = useUserStore();
            userStore.updateOnboardedStatus(true);
            toast.success(data.message || 'User info updated successfully.');
            return true;
        }
        toast.error(data.message || 'Something went wrong.');
    } catch (error) {
        toast.error('Something went wrong.');
    }

    return false;
};

export default submitOnboardingForm;
