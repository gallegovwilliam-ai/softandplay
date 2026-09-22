
$("#id_telefono").on('input', function() {  //this is use for every time input change.
        var inputValue = getInputValue(); //get value from input and make it usefull number
        var length = inputValue.length; //get lenth of input
        if (inputValue < 1000)
        {
            inputValue = '57('+inputValue;
        }else if (inputValue < 1000000) 
        {
            inputValue = '57('+ inputValue.substring(0, 3) + ')' + inputValue.substring(3, length);
        }else if (inputValue < 10000000000) 
        {
            inputValue = '57('+ inputValue.substring(0, 3) + ')' + inputValue.substring(3, 6) + '-' + inputValue.substring(6, length);
        }else
        {
            inputValue = '57('+ inputValue.substring(0, 3) + ')' + inputValue.substring(3, 6) + '-' + inputValue.substring(6, 10);
        }       
        $("#id_telefono").val(inputValue); //correct value entered to your input.
        inputValue = getInputValue();//get value again, becuase it changed, this one using for changing color of input border
       if ((inputValue > 2000000000) && (inputValue < 9999999999))
      {
          $("#id_telefono").css("border","#C7C7CC solid 1px");//if it is valid phone number than border will be black.
      }else
      {
          $("#id_telefono").css("border","red solid 1px");//if it is invalid phone number than border will be red.
      }
  });

    function getInputValue() {
         var inputValue = $("#id_telefono").val().replace(/\D/g,'');  //remove all non numeric character
        if (inputValue.charAt(0) == 5) // if first character is 1 than remove it.
        {
            var inputValue = inputValue.substring(2, inputValue.length);
        }
        return inputValue;
}

/**** SETTINGS AJAX ****/

    $(document).ajaxStart(function() {
        $(':button[type="submit"]').html('<img src="https://www.thepalmsatweston.com/Content/images/loader.gif" width="20px">');
        $(':button[type="submit"]').attr('disabled','disabled');   
        $(':button[type="button"]').attr('disabled','disabled');   
    });
    $(document).ajaxStop(function() {
        $(':button[type="submit"]').html('Guardar');
        $(':button[type="submit"]').removeAttr('disabled');
        $(':button[type="button"]').removeAttr('disabled');
    });

/**** COMTROL DE ERRORES ****/
function scrollToID(element,idError,msj){
  $(idError).show();
  $(idError + 'BR').show();
  $(idError + ' span').html(msj);
  $('html, body').animate({
        scrollTop: $(idError).offset().top - 100
    }, 'slow');
  $(element).css('border','2px solid red');
}

//ESCONDE EL SALTO DE LINEA
function ErrorHide(idError){
  $(idError).hide();
  $(idError + 'BR').hide();

}

/**** ENVIAR AJAX DE CREAR USUARIO ****/
$( "#addUsuario" ).submit(function( event ) {

if($('#id_first_name').val()==''){
    scrollToID('#id_first_name','#ErrorNombre','Debe ingresar el Nombre');
    return false;
  }else{
    ErrorHide('#ErrorNombre');
    $('#id_first_name').css('border','1px solid #C7C7CC');
  }

  if($('#id_last_name').val()==''){
    scrollToID('#id_last_name','#ErrorApellido','Debe ingresar el Apellido');
    return false;
  }else{
    ErrorHide('#ErrorApellido');
    $('#id_last_name').css('border','1px solid #C7C7CC');
  }

  if($('#id_telefono').val()==''){
    scrollToID('#id_telefono','#ErrorTelefono','Debe ingresar el Teléfono');
    return false;
  }else{
    ErrorHide('#ErrorTelefono');
    $('#id_telefono').css('border','1px solid #C7C7CC');
  }

  if($('#id_username').val()==''){
    scrollToID('#id_username','#ErrorNick','Debe ingresar el Username');
    $('#id_username').css('border','2px solid red');
    return false;
  }else{
    ErrorHide('#ErrorNick');
    $('#id_username').css('border','1px solid #C7C7CC');
  }

  if($('#id_email').val()==''){
    scrollToID('#id_email','#ErrorEmail','Debe ingresar el Email');
    $('#id_email').css('border','2px solid red');
    return false;
  }else{
    ErrorHide('#ErrorEmail');
    $('#id_email').css('border','1px solid #C7C7CC');
  }


if( !validateEmail($('#id_email').val())) { 
  scrollToID('#id_email','#ErrorEmail','Debe ingresar un Email Valido');
  $('#id_email').css('border','2px solid red');
  return false;  
}else{
  ErrorHide('#ErrorEmail');
  $('#id_email').css('border','1px solid #C7C7CC');  
}


  var formData = new FormData();
  formData.append('username',$('#id_username').val());
  formData.append('first_name',$('#id_first_name').val());
  formData.append('last_name',$('#id_last_name').val());
  formData.append('telefono',$('#id_telefono').val());
  formData.append('email',$('#id_email').val());
  formData.append('sala',$('#id_sala').val());
  formData.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
  if($('#id_thumb').val()!=""){
    formData.append('file', $('#id_thumb')[0].files[0]);
  }
  

   $.ajax({
           type: "POST",
           url: '/usuario/crear/',
           enctype: 'multipart/form-data',         
           data: formData, // serializes the form's elements.
           processData: false,  // tell jQuery not to process the data
           contentType: false,  // tell jQuery not to set contentType           
           success: function(data)
           {

              if(data=='ok'){
                 setTimeout("location.href='/usuario/'", 500);
              }else if(data=='existeEmail'){
                scrollToID('#id_email','#ErrorEmail','El email esta registrado');
              }else if(data=='existeUser'){
                scrollToID('#id_username','#ErrorNick','El usuario existe');
              
              }
           }
         });
  event.preventDefault();
});



/**** ENVIAR AJAX DE EDITAR USUARIO ****/
$( "#editUsuario" ).submit(function( event ) {

if($('#id_first_name').val()==''){
    scrollToID('#id_first_name','#ErrorNombre','Debe ingresar el Nombre');
    return false;
  }else{
    ErrorHide('#ErrorNombre');
    $('#id_first_name').css('border','1px solid #C7C7CC');
  }

  if($('#id_last_name').val()==''){
    scrollToID('#id_last_name','#ErrorApellido','Debe ingresar el Apellido');
    return false;
  }else{
    ErrorHide('#ErrorApellido');
    $('#id_last_name').css('border','1px solid #C7C7CC');
  }

  if($('#id_telefono').val()==''){
    scrollToID('#id_telefono','#ErrorTelefono','Debe ingresar el Teléfono');
    return false;
  }else{
    ErrorHide('#ErrorTelefono');
    $('#id_telefono').css('border','1px solid #C7C7CC');
  }


  if($('#id_username').val()==''){
    scrollToID('#id_username','#ErrorNick','Debe ingresar el Username');
    $('#id_username').css('border','2px solid red');
    return false;
  }else{
    ErrorHide('#ErrorNick');
    $('#id_username').css('border','1px solid #C7C7CC');
  }

  if($('#id_email').val()==''){
    scrollToID('#id_email','#ErrorEmail','Debe ingresar el Email');
    $('#id_email').css('border','2px solid red');
    return false;
  }else{
    ErrorHide('#ErrorEmail');
    $('#id_email').css('border','1px solid #C7C7CC');
  }


if( !validateEmail($('#id_email').val())) { 
  scrollToID('#id_email','#ErrorEmail','Debe ingresar un Email Valido');
  $('#id_email').css('border','2px solid red');
  return false;  
}else{
  ErrorHide('#ErrorEmail');
  $('#id_email').css('border','1px solid #C7C7CC');  
}

  var formData = new FormData();
  formData.append('id',$('#id_id').val());
  formData.append('username',$('#id_username').val());
  formData.append('first_name',$('#id_first_name').val());
  formData.append('last_name',$('#id_last_name').val());
  formData.append('telefono',$('#id_telefono').val());
  formData.append('email',$('#id_email').val());
  formData.append('sala',$('#id_sala').val());
  formData.append('csrfmiddlewaretoken', $("input[name='csrfmiddlewaretoken']").val());
  if($('#id_thumb').val()!=""){
    formData.append('file', $('#id_thumb')[0].files[0]);
  }


   $.ajax({
           type: "POST",
           url: '/usuario/editar/' + $('#id_id').val() + '/',
           enctype: 'multipart/form-data',         
           data: formData, // serializes the form's elements.
           processData: false,  // tell jQuery not to process the data
           contentType: false,  // tell jQuery not to set contentType           
           success: function(data)
           {

              if(data=='existeEmail'){
                scrollToID('#id_email','#ErrorEmail','El email esta registrado');
              }else if(data=='existeUser'){
                scrollToID('#id_username','#ErrorNick','El usuario existe');
              
              }else if(data=='ok'){
                  setTimeout("location.href='/usuario/'", 500);
              }
           }
         });
  event.preventDefault();
});


//BORRAR ITEM //
function BorrarUser(id,csrf_token){

 if (confirm('¿Estas seguro de eliminar el Usuario?')) {
           $.ajax({
                   type: "POST",
                   url: '/usuario/eliminar/' + id + '/',
                   data: { 'pk' : id,'csrfmiddlewaretoken': csrf_token },

                   success: function(data)
                   {
                      if(data=='ok'){
                          alert('Eliminado exitosamente');
                          $("#" + id + "_fila").fadeOut("slow");
                      }
                   }
                 });
    }

    return false;

}

/**** VALIDAR EMAIL ****/
 function validateEmail($email) {
  var emailReg = /^([\w-\.]+@([\w-]+\.)+[\w-]{2,4})?$/;
  return emailReg.test( $email );
}
