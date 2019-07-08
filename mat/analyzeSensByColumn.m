%script que recolecta las matrices de errores o factor de costo y las
%procesa para determinar por columna si un parametro es sensible o no ante
%un umbral determinado. Contemplando esto, se crea un conjunto de datos por
%cada parametro con respecto a un umbral de corte, este umbral varia y es
%recibido por argumento, la idea es crear diferentes matrices con
%diferentes umbrales para analizar por un lado tendencias de sensibilidad,
%etc. Se exporta junto con el ID del paciente al cual esta asociado
function analyzeSensByColumn(umbral, exportPath)
    
    %cantidad de columnas
    for i=1:21
        matrixResponse = [];%matriz utilizada para exportar la data
        for paciente=1:462
            
            %try
                nameMat = "VarParP_"+paciente+"_GP2.mat";%cargamos la data
                load(nameMat);                        
                row = [];%definimos una row
                matrixResponse(paciente, 1) = paciente;%agregamos el ID del sujeto
                for param=1:16
                    if M(param,i)>=umbral
                        matrixResponse(paciente, param+1) = 1;%supera el umbral
                    else
                        matrixResponse(paciente, param+1) = 0;%no supera el umbral
                    end
                end
                
            %catch
                %paciente no ajustado
             %   for index=1:16
             %       matrixResponse(paciente,index) = -1;%no ajustado
             %   end
            %end                        
        end
        
        %exportamos el documento
        nameDoc = exportPath+"sensibleCol_"+i+".csv";
        csvwrite(nameDoc, matrixResponse);
    end    
end