def importe_total_carro(request):
    total=0

    try:
      if request.user.is_authenticated:  
        for key, value in request.session["carro"].items():
          total = total + (int(value["precio"]) * value["cantidad"])
          cantidad = value["cantidad"]
      else:
        pass
    except:
      pass
    return {'importe_total_carro':total}
