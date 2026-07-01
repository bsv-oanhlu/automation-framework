class CheckoutInfoLocators:
    FIRST_NAME = "#first-name"
    LAST_NAME = "#last-name"
    POSTAL_CODE = "#postal-code"
    CONTINUE = "#continue"
    CANCEL = "#cancel"


class CheckoutOverviewLocators:
    ITEM_TOTAL = ".summary_subtotal_label"
    TAX = ".summary_tax_label"
    TOTAL = ".summary_total_label"
    PAYMENT_INFO = '[data-test="payment-info-label"] + [data-test="payment-info-value"]'
    SHIPPING_INFO = '[data-test="shipping-info-label"] + [data-test="shipping-info-value"]'
    FINISH = "#finish"
    CANCEL = "#cancel"


class CheckoutCompleteLocators:
    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    PONY_EXPRESS = ".pony_express"
    BACK_HOME = "#back-to-products"
