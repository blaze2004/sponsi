
const setLoading=({ loading, element }) => {
    element.dataset.loading=loading;
}

const callApi=async ({ url, options={}, loadingElementId=null, refreshOnSuccess=false }) => {

    const loadingElement=loadingElementId? document.getElementById(loadingElementId):null;
    if (loadingElement) {
        setLoading({ loading: true, element: loadingElement });
    }

    try {
        const response=await fetch(url, {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            }
        });

        const data=await response.json();

        if (response.ok) {

            if (refreshOnSuccess) {
                window.location.reload();
            }
            showToast({ message: data.message, category: 'success' });
            return;
        }
        showToast({ message: data.message, category: 'danger' });
    } catch (error) {
        console.error(error);
        showToast({ message: "Something bad happened, please try again.", category: 'danger' });
    } finally {
        if (loadingElementId) {
            setLoading({ loading: false, element: loadingElement });
        }
    }
}

const showToast=({ message, category }) => {

    const toastId='toast-'+Date.now();
    const toast=document.createElement('div');
    toast.id=toastId;
    toast.classList.add('toast', 'align-items-center', 'border-0');
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.classList.add(`text-bg-${category}`);

    toast.innerHTML=`
    <div class="d-flex">
        <div class="toast-body">
        ${message}
        </div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>`;

    document.querySelector(".toast-container").appendChild(toast);

    new window.bootstrap.Toast(toast).show();
}