document.addEventListener('DOMContentLoaded', () => {
    // Select DOM elements
    const selectAll = document.getElementById('select-all');
    const selectAllFooter = document.getElementById('select-all-footer');
    const shopCheckbox = document.getElementById('shop-checkbox');
    const productCheckboxes = document.querySelectorAll('.product-checkbox');
    const productItems = document.querySelectorAll('.product-item');
    const totalItemsSpan = document.getElementById('total-items');
    const selectedItemsSpan = document.getElementById('selected-items');
    const totalPriceSpan = document.getElementById('total-price');
    const removeSelectedBtn = document.getElementById('remove-selected');

    
    console.log('selectAll:', selectAll);
    console.log('selectAllFooter:', selectAllFooter);
    console.log('shopCheckbox:', shopCheckbox);
    console.log('productCheckboxes:', productCheckboxes);

  
    const formatPrice = (price) => {
        return `₫${price.toLocaleString('vi-VN')}`;
    };

    const calculateTotal = () => {
        let total = 0;
        let selectedCount = 0;

        productItems.forEach(item => {
            const checkbox = item.querySelector('.product-checkbox');
            if (checkbox.checked) {
                const price = parseInt(item.getAttribute('data-price')) || 0;
                const quantity = parseInt(item.querySelector('.quantity-input').value);
                total += price * quantity;
                selectedCount++;
            }
        });

        selectedItemsSpan.textContent = selectedCount;
        totalPriceSpan.textContent = formatPrice(total);
    };


    const updateProductTotal = (item) => {
        const price = parseInt(item.getAttribute('data-price')) || 0;
        const quantity = parseInt(item.querySelector('.quantity-input').value);
        const totalPrice = price * quantity;
        item.querySelector('.total-price').textContent = formatPrice(totalPrice);
        calculateTotal();
    };

    const toggleSelectAll = (event) => {
        const isChecked = event.target.checked;
        console.log('Toggle Select All triggered, isChecked:', isChecked);

        productCheckboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });

        if (shopCheckbox) {
            shopCheckbox.checked = isChecked;
        }

        if (selectAll) selectAll.checked = isChecked;
        if (selectAllFooter) selectAllFooter.checked = isChecked;

        calculateTotal();
    };

    if (selectAll) {
        selectAll.addEventListener('change', toggleSelectAll);
    } else {
        console.error('selectAll element not found');
    }

    if (selectAllFooter) {
        selectAllFooter.addEventListener('change', toggleSelectAll);
    } else {
        console.error('selectAllFooter element not found');
    }

    if (shopCheckbox) {
        shopCheckbox.addEventListener('change', () => {
            const isChecked = shopCheckbox.checked;
            console.log('Shop Checkbox changed, isChecked:', isChecked);

            productCheckboxes.forEach(checkbox => {
                checkbox.checked = isChecked;
            });

            const allChecked = Array.from(productCheckboxes).every(cb => cb.checked);
            if (selectAll) selectAll.checked = allChecked;
            if (selectAllFooter) selectAllFooter.checked = allChecked;
            calculateTotal();
        });
    } else {
        console.error('shopCheckbox element not found');
    }

    productCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const allChecked = Array.from(productCheckboxes).every(cb => cb.checked);
            console.log('Individual checkbox changed, allChecked:', allChecked);

            if (selectAll) selectAll.checked = allChecked;
            if (selectAllFooter) selectAllFooter.checked = allChecked;
            if (shopCheckbox) {
                shopCheckbox.checked = allChecked;
            }
            calculateTotal();
        });
    });

    productItems.forEach(item => {
        const decreaseBtn = item.querySelector('.decrease');
        const increaseBtn = item.querySelector('.increase');
        const quantityInput = item.querySelector('.quantity-input');

        decreaseBtn.addEventListener('click', () => {
            let quantity = parseInt(quantityInput.value);
            if (quantity > 1) {
                quantityInput.value = quantity - 1;
                updateProductTotal(item);
            }
        });

        increaseBtn.addEventListener('click', () => {
            let quantity = parseInt(quantityInput.value);
            quantityInput.value = quantity + 1;
            updateProductTotal(item);
        });

        quantityInput.addEventListener('input', () => {
            let value = parseInt(quantityInput.value) || 1;
            if (value < 1) value = 1;
            quantityInput.value = value;
            updateProductTotal(item);
        });
    });

    productItems.forEach(item => {
        const removeBtn = item.querySelector('.remove');
        removeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            if (confirm('Bạn có chắc muốn xóa sản phẩm này?')) {
                item.remove();
                totalItemsSpan.textContent = document.querySelectorAll('.product-item').length;
                calculateTotal();
            }
        });
    });

    removeSelectedBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (confirm('Bạn có chắc muốn xóa các sản phẩm đã chọn?')) {
            productItems.forEach(item => {
                const checkbox = item.querySelector('.product-checkbox');
                if (checkbox.checked) {
                    item.remove();
                }
            });
            totalItemsSpan.textContent = document.querySelectorAll('.product-item').length;
            if (selectAll) selectAll.checked = false;
            if (selectAllFooter) selectAllFooter.checked = false;
            if (shopCheckbox) {
                shopCheckbox.checked = false;
            }
            calculateTotal();
        }
    });

    totalItemsSpan.textContent = productItems.length;
    calculateTotal();

   
    const adMainSlider = document.querySelector('.ad-main-slides');
    const adMainSlides = document.querySelectorAll('.ad-main-slide');
    const adMainPrevBtn = document.querySelector('.ad-main-prev');
    const adMainNextBtn = document.querySelector('.ad-main-next');
    const adMainDots = document.querySelectorAll('.main-dot');
    let currentMainAdIndex = 0;

    const showMainAdSlide = (index) => {
        adMainSlides.forEach((slide, i) => {
            slide.classList.remove('active');
            adMainDots[i].classList.remove('active');
            if (i === index) {
                slide.classList.add('active');
                adMainDots[i].classList.add('active');
            }
        });
    };

    const nextMainAdSlide = () => {
        currentMainAdIndex = (currentMainAdIndex + 1) % adMainSlides.length;
        showMainAdSlide(currentMainAdIndex);
    };

    const prevMainAdSlide = () => {
        currentMainAdIndex = (currentMainAdIndex - 1 + adMainSlides.length) % adMainSlides.length;
        showMainAdSlide(currentMainAdIndex);
    };

    let autoMainSlide = setInterval(nextMainAdSlide, 5000);

    if (adMainSlider) {
        adMainSlider.addEventListener('mouseenter', () => {
            clearInterval(autoMainSlide);
        });

        adMainSlider.addEventListener('mouseleave', () => {
            autoMainSlide = setInterval(nextMainAdSlide, 5000);
        });
    }

    if (adMainPrevBtn) {
        adMainPrevBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            prevMainAdSlide();
        });
    }

    if (adMainNextBtn) {
        adMainNextBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            nextMainAdSlide();
        });
    }

    adMainDots.forEach((dot, index) => {
        dot.addEventListener('click', (e) => {
            e.stopPropagation();
            currentMainAdIndex = index;
            showMainAdSlide(currentMainAdIndex);
        });
    });

    showMainAdSlide(currentMainAdIndex);

    // Chat functionality
    const chatIcon = document.querySelector('.chat-icon');
    const chatWindow = document.getElementById('chat-window');
    const chatCloseBtn = document.querySelector('.chat-close-btn');

    console.log('chatIcon:', chatIcon);
    console.log('chatWindow:', chatWindow);
    console.log('chatCloseBtn:', chatCloseBtn);

    if (chatIcon) {
        chatIcon.addEventListener('click', (e) => {
            e.stopPropagation();
            console.log('Chat icon clicked');
            if (chatWindow) {
                chatWindow.classList.toggle('active');
            } else {
                console.error('chatWindow not found when clicking chatIcon');
            }
        });
    } else {
        console.error('chatIcon not found');
    }

    if (chatCloseBtn) {
        chatCloseBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            console.log('Close button clicked');
            if (chatWindow) {
                chatWindow.classList.remove('active');
            }
        });
    } else {
        console.error('chatCloseBtn not found');
    }
});
