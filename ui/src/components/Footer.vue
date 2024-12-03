<template>
    <div class="w-full border-top py-3 text-center">
        <div class="mx-auto max-w-screen-xl px-4 d-flex flex-column flex-sm-row justify-content-between align-items-center">
            <div class="text-center text-sm-start">
                <p class="text-sm">&copy; {{ year }} Sponsi. All rights reserved.</p>
            </div>
            <div class="d-flex flex-column mt-4 mt-sm-0 flex-sm-row" style="gap: 4px">
                <a href="https://github.com/blaze2004/sponsi" class="btn btn-ghost">Contribute</a>
                <a href="https://www.buymeacoffee.com/blaze2004" class="btn btn-ghost">Donate</a>
                <a href="mailto:22f3001541@ds.study.iitm.ac.in" class="btn btn-ghost"> Contact Us </a>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            year: new Date().getFullYear(),
        };
    },
};
</script>
