module.exports={
    apps: [
        {
            name: 'backend',
            script: 'python',
            args: 'main.py',
        },
        {
            name: 'frontend',
            script: 'pnpm vite',
        }
    ]
};
