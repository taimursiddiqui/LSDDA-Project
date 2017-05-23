import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class CSV_TO_JSON {

	public static void main(String[] args) throws IOException {
		try {
			Scanner sc  = new Scanner(new File("bbc_dataset.csv"));
			FileWriter file = new FileWriter("bbc_dataset.json");
			sc.nextLine(); // skipping first line where field names are written
			int i=0;
			while (sc.hasNextLine()){
				String fields[] = (sc.nextLine()).split(",");
				if(fields.length==13){ // If there are less or greater than 13 fields then simply skip that record.
					boolean isEmpty = false;
					for(int j=0; j<fields.length; j++){
						if((fields[j].trim()).equals("") && j!=9){ // if brand_id is empty then its okay
							isEmpty = true;
							break;
						}
					}
					if(!isEmpty){
						
						String[] titles = (((fields[5].replaceAll("\"", "")).replaceAll("_", " ")).toLowerCase()).split(":");
						String complete_title = "\"\"";
						int len  = titles.length;
						if(len==1)
							complete_title = "{\"episode\": \""+(titles[0].trim())+"\"}";
						else if(len==2)
							complete_title = "{\"series_title\": \""+(titles[0].trim())+"\", " + "\"episode\": \""+(titles[1].trim())+"\"}";
						else if(len==3)
							complete_title = "{\"series\": \""+(titles[0].trim())+"\", " + "\"series_title\": \""+(titles[1].trim())+"\", "+
											   "\"episode\": \""+(titles[2].trim())+"\"}";
						else if(len>=4)
							complete_title = "{\"brand\": \""+(titles[len-4].trim())+"\", " + "\"series\": \""+(titles[len-3].trim())+"\", "+
											"\"series_title\": \""+(titles[len-2].trim())+"\", " + "\"episode\": \""+(titles[len-1].trim())+"\"}";
						
						String separtedCategories = "[";
						String[] categories = (((fields[11].substring(1, fields[11].length()-1)).replaceAll("_", " ")).toLowerCase()).split("\\.");
						if(!categories[0].equals("")){
							  for(String category : categories){
								  String[] mixed_material = category.split(":");
								  separtedCategories = separtedCategories + "\""+(mixed_material[mixed_material.length-1].trim())+"\", ";
							  }
							  separtedCategories = separtedCategories.substring(0, separtedCategories.length()-2);
						}
						separtedCategories = separtedCategories + "]";
						
						
						String separtedTags = "[";
						String[] tags = ((fields[12].substring(1, fields[12].length()-1)).toLowerCase()).split("\\.");
						if(!tags[0].equals("")){
							  for(String tag : tags){
								  separtedTags = separtedTags + "\""+tag+"\", ";
							  }
							  separtedTags = separtedTags.substring(0, separtedTags.length()-2);
						}
						separtedTags = separtedTags + "]";
						
						String JSON_document  = "{\"pid\": \""    +fields[0]+"\", "+
										"\"epoch_start\": "    +fields[3]+", "+
										"\"epoch_end\": "      +fields[4]+", "+
										"\"complete_title\": " +complete_title+", "+
										"\"media_type\": \""   +fields[6].toLowerCase()+"\", "+
										"\"masterbrand\": \""  +fields[7].toLowerCase()+"\", "+
										"\"service\": \""	   +fields[8].toLowerCase()+"\", "+
										"\"brand_pid\": \""	   +fields[9]+"\", "+
										"\"is_clip\": "        +fields[10]+", "+
										"\"categories\": "     +separtedCategories+", "+
										"\"tags\": "           +separtedTags+ "}";
						
						
				        
						file.write(JSON_document+"\n");
						
						i++;
						/*if(i==20)
							break;*/
					
					} // if isEmpty ends
				
				} // if 13-fields ends
				
				
			} // while ends
			
			
	        file.flush();
			System.out.println("count="+ i);
			
			
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		

	}

}