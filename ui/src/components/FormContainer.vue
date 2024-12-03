<template>
    <div class="d-flex justify-content-center align-items-center p-2 min-h-screen">
        <div class="w-full max-w-md">
            <div class="rounded-lg border border-border bg-card text-card-foreground shadow-sm">
                <div class="d-flex flex-column gap-2 p-4">
                    <h3 class="h4 font-weight-bold m-0">
                        {{ title }}
                    </h3>
                </div>
                <div class="p-4 pt-0">
                    <slot></slot>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        title: {
            type: String,
        },
    },
};
</script>
