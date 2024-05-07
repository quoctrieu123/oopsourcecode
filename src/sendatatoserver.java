
import java.io.*;
import java.net.*;
import org.json.simple.*;
import org.json.simple.parser.*;
public class sendatatoserver 
{  
    public JSONArray printserver(String input){
    try {
            
            URL url = new URL("http://localhost:5000/data"); // URL của API server Flask
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);

            OutputStream os = conn.getOutputStream();
            os.write(input.getBytes());
            os.flush();

            if (conn.getResponseCode() != HttpURLConnection.HTTP_OK) {
                throw new RuntimeException("Failed: HTTP error code: " + conn.getResponseCode());
            }

            BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));
            
            String output;
            String result="";
            while ((output = br.readLine()) != null) {
            	result+=output;
            }
            String jsonString= result;
            try
            {
		JSONParser jsonParser = new JSONParser();
		JSONArray jsonArray = (JSONArray) jsonParser.parse(jsonString);
		return jsonArray;
             
             
            }
		
		
		

		
            catch (ParseException e) 
            {
                e.printStackTrace();
                return null;
            }
        }
    catch (Exception ex) 
    {
        ex.printStackTrace();
        return null;
    }
    }
}
