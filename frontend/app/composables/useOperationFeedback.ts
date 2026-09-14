import {
  ref
} from 'vue'


export const useOperationFeedback = () => {

  const operationError =
    ref('')

  const successMessage =
    ref('')


  const clearFeedback = () => {

    operationError.value = ''

    successMessage.value = ''
  }


  const setError = (
    message: string
  ) => {

    operationError.value =
      message

    successMessage.value = ''
  }


  const setSuccess = (
    message: string
  ) => {

    successMessage.value =
      message

    operationError.value = ''
  }


  return {
    operationError,
    successMessage,

    clearFeedback,
    setError,
    setSuccess
  }
}