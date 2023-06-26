import {Modal} from "bootstrap";
import {Dropdown} from "bootstrap"

export default defineNuxtPlugin(() => ({
    provide: {
        bootstrap: {
            Modal,
            Dropdown,
        }
    },
}));