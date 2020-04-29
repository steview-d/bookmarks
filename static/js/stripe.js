$(function() {
    $("#payment-form").submit(function() {
        var form = this;
        var card = {
            number: $("#id_credit_card_number").val(),
            expMonth: $("#id_expiry_month").val(),
            expYear: $("#id_expiry_year").val(),
            cvc: $("#id_cvv").val(),
        };

        Stripe.createToken(card, function(status, response) {
            // Check payment details with the Stripe api
            if (status === 200) {
                /*
                Additional checks due to how Stripe test mode handles
                the CVV number and certain card numbers.
                If card length is not 16 digits, and CVV is not 3 digits,
                do not process payment, instead return an error.
                These 2 checks are for test mode only and can be removed
                for live payments
                */
                if ($("#id_credit_card_number")[0].value.length != 16) {
                    showStripeErrors("Your card number is incorrect");
                } else if ($("#id_cvv")[0].value.length != 3) {
                    showStripeErrors("Your card's security code is invalid.");
                } else {
                    $("#credit-card-errors").hide();
                    $("#id_stripe_id").val(response.id);
    
                    // Prevent CC details from being submitted to the server
                    $("#id_credit_card_number").removeAttr("name");
                    $("#id_cvv").removeAttr("name");
                    $("#id_expiry_month").removeAttr("name");
                    $("#id_expiry_year").removeAttr("name");
    
                    form.submit();
                }

            } else {
                showStripeErrors(response.error.message);
            }
        });

        return false;
    });
});

function showStripeErrors (errorText) {
    // Show errors above payment form
    $("#stripe-error-message").text(errorText);
    $("#credit-card-errors").show();
    $("#validate_card_btn").attr("disabled", false);
}