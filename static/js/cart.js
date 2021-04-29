// get the buttons for class 'update-cart'
var updateBtns = document.getElementsByClassName('update-cart')

// add click eventListener to all the buttons
for(i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        // get the product id and the action from the custom data set in the html
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId: ', productId, 'action: ', action)

        // now to check the user
        console.log('User type:', user)
        if(user == 'AnonymousUser'){
            console.log('Guest User')
        }
        else{
            updateItem(productId, action)
        }
    })
}

function updateItem(productId, action){
        // API fetch to post productID and action to the views.py to
        // add the specific item in the cart and increase quantity (mi lord)
        var url = '/update-item/'

        fetch(
            url,
            {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken': csrftoken,
                },
                body:JSON.stringify({
                    'productId':productId, 
                    'action':action,
                })
            })
            .then((response) => {
                return response.json();
            }) 
            .then((data) => { 
                console.log('data:', data)
                location.reload()
            })
}