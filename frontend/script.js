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

    // Function to calculate total price
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

    // Function to update individual product total
    const updateProductTotal = (item) => {
        const price = parseInt(item.getAttribute('data-price')) || 0;
        const quantity = parseInt(item.querySelector('.quantity-input').value);
        const totalPrice = price * quantity;
        item.querySelector('.total-price').textContent = formatPrice(totalPrice);
        calculateTotal();
    };

    // Select All functionality
    const toggleSelectAll = (event) => {
        const isChecked = event.target.checked;
        console.log('Toggle Select All triggered, isChecked:', isChecked);

       
        productCheckboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });

    
        if (shopCheckbox) {
            shopCheckbox.checked = isChecked;
        }

        selectAll.checked = isChecked;
        selectAllFooter.checked = isChecked;

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
            console.log('Shop Checkbox changed, isChecked:', isChecked); // Debugging

            productCheckboxes.forEach(checkbox => {
                checkbox.checked = isChecked;
            });

            const allChecked = Array.from(productCheckboxes).every(cb => cb.checked);
            selectAll.checked = allChecked;
            selectAllFooter.checked = allChecked;
            calculateTotal();
        });
    } else {
        console.error('shopCheckbox element not found');
    }

    // Individual checkbox change
    productCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const allChecked = Array.from(productCheckboxes).every(cb => cb.checked);
            console.log('Individual checkbox changed, allChecked:', allChecked); // Debugging

            selectAll.checked = allChecked;
            selectAllFooter.checked = allChecked;
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

    // Remove individual product
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

    // Remove selected products
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
            selectAll.checked = false;
            selectAllFooter.checked = false;
            if (shopCheckbox) {
                shopCheckbox.checked = false;
            }
            calculateTotal();
        }
    });

    // Initial calculation
    totalItemsSpan.textContent = productItems.length;
    calculateTotal();
});
