package com.tcs.controllers;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.servlet.ModelAndView;

/**
 * A controller that provides entry to the application
 * for testing Mustache views 
 * 
 * @author Arun Ramachandran
 *
 */
@Controller
public class ApplicationController {
	
	@RequestMapping(value="/test", method=RequestMethod.GET)
	public ModelAndView test() {
		ModelAndView modelAndView = new ModelAndView("test");
		modelAndView.addObject("title", "Testing Mustache with Model And View");
		modelAndView.addObject("name", "Mustache");
		modelAndView.addObject("something", "Mustache");
		
		String[] strArr = {"one","two","three"};
		modelAndView.addObject("lst", Arrays.asList(strArr));
		
		Map<String, String> testMap = new HashMap<String, String>();
		testMap.put("name", "testMap");
		testMap.put("context", "\"Map Context\"");
		testMap.put("block_name", "\"mappedValues\"");
		
		modelAndView.addObject("mappedValues",testMap);
		
		return modelAndView;
	}

}
