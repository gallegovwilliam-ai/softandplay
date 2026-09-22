
/**** SETTINGS AJAX ****/
    $(document).ajaxStart(function() {
        $(':button[type="submit"]').html('<img src="https://www.thepalmsatweston.com/Content/images/loader.gif" width="20px">');
        $(':button[type="submit"]').attr('disabled','disabled');   
        $(':button[type="button"]').attr('disabled','disabled');   
    });
    $(document).ajaxStop(function() {
        $(':button[type="submit"]').html('Generar');
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

/**** ENVIAR AJAX DE Reporte ****/
$( "#reportSala" ).submit(function( event ) {



// if($('#id_fecha').val()==''){
//     scrollToID('#id_fecha','#ErrorFecha','Debe indicar la Fecha');
//     return false;
//   }else{
//     ErrorHide('#ErrorFecha');
//     $('#id_fecha').css('border','1px solid #C7C7CC');
//   }


  $.ajax({
           type: "POST",
           url: '/reportes/salas2/',
           data: $( "#reportSala" ).serialize(), // serializes the form's elements.           
           success: function(data)
           {

             if(data=='ok'){
                  setTimeout("location.href='/partida/'", 300);

              }else{
                alert(data);
              }
           }
         });
  event.preventDefault();
});



/**** ENVIAR AJAX DE Reporte ****/
$( "#reportFinanzas" ).submit(function( event ) {



  // if($('#id_fecha').val()==''){
  //     scrollToID('#id_fecha','#ErrorFecha','Debe indicar la Fecha');
  //     return false;
  //   }else{
  //     ErrorHide('#ErrorFecha');
  //     $('#id_fecha').css('border','1px solid #C7C7CC');
  //   }
  
  
    $.ajax({
             type: "POST",
             url: '/reportes/finanzas-total/',
             data: $( "#reportFinanzas" ).serialize(), // serializes the form's elements.           
             success: function(data)
             {
  
               if(data=='ok'){
                    setTimeout("location.href='/partida/'", 300);
  
                }else{
                  alert(data);
                }
             }
           });
    event.preventDefault();
  });
  