function processData(threshold, tresholdFreq, nameExport)
    
    matrixResponse = [];
    for paciente=1:462  
        try
            nameMat = "VarParP_"+paciente+"_GP2.mat";
            load(nameMat);                        
            for i=1:16
                contSensible = 0;        
                for j=1:21
                    if (M(i,j) >= threshold)
                        contSensible = contSensible+1;%contamos sensibilidad segun el umbral inicial
                    end
                end
                data = contSensible/20;%obtenemos la frecuencia
                
                if data >=tresholdFreq
                    matrixResponse(paciente,i) = 1;%sensible
                else
                    matrixResponse(paciente,i) = 0;%no sensible
                end
            end
        catch
            for i=1:16
                matrixResponse(paciente,i) = -1;%no ajustado
            end
        end
        
    end
    csvwrite(nameExport, matrixResponse);
end