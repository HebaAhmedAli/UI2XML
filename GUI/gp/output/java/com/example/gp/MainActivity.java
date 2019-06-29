package com.example.gp;
import android.os.Bundle;
import android.view.View;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.ActionBar;

public class MainActivity extends AppCompatActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		this.getSupportActionBar().setDisplayOptions(ActionBar.DISPLAY_SHOW_CUSTOM);
		getSupportActionBar().setDisplayShowCustomEnabled(true);
		getSupportActionBar().setCustomView(R.layout.action_bar_main);
		View view = getSupportActionBar().getCustomView();
	}
	public void clickMe0_0_0(View view){
	// onClick logic
		Toast.makeText(getApplicationContext(),"Clicked on Button0_0_0",Toast.LENGTH_SHORT).show();
	}
	public void clickMe0_4_0(View view){
	// onClick logic
		Toast.makeText(getApplicationContext(),"Clicked on Button0_4_0",Toast.LENGTH_SHORT).show();
	}
	public void clickMe0_5_0(View view){
	// onClick logic
		Toast.makeText(getApplicationContext(),"Clicked on Button0_5_0",Toast.LENGTH_SHORT).show();
	}
	public void clickMe0_6_0(View view){
	// onClick logic
		Toast.makeText(getApplicationContext(),"Clicked on Button0_6_0",Toast.LENGTH_SHORT).show();
	}
}